# Import the necessary libraries
import cv2
from ultralytics import YOLO
import av
import numpy as np
import streamlit as st
from PIL import Image
import os
import tempfile
from io import BytesIO
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase


# Titre de l'application
st.title("Détection d'objets avec YOLOv5")
st.write("""
Ce programme utilise le modèle YOLOv5 pour détecter les objets dans une image, une vidéo ou en direct avec la webcam.
Il peut détecter plusieurs objets en quelques millisecondes et afficher des statistiques sur les objets détectés.
""")

# Section À propos
with st.expander("À propos de cette application"):
    st.write("""
    Cette application permet de détecter des objets dans :
    - **Images** : Téléchargez une image et voyez les objets détectés.
    - **Vidéos** : Chargez une vidéo et observez la détection frame par frame.
    - **Webcam** : Activez votre webcam pour une détection en temps réel.
    """)


# Chargement du modèle YOLOv5
try:
    model = YOLO('yolov5su.pt')
except Exception as e:
    st.error("Erreur lors du chargement du modèle YOLOv5")
    st.write(e)
    st.stop()

# Choix de la source d'entrée
input_type = st.sidebar.selectbox(
    "Source de l'entrée :",
    ("Image", "Webcam", "Vidéo"),
    key="input_type",
    placeholder="Choisir le type de données d'entrée"
)
#############################################
# webcam utils function
#############################################
def callback_function(frame): 
    img = frame.to_ndarray(format="bgr24")
    results = model(img)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f"{model.names[int(box.cls[0])]} {box.conf[0]:.2f}"
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            img = cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return av.VideoFrame.from_ndarray(img, format="bgr24")


# Détection sur une image
if input_type == "Image":
    img_file = st.file_uploader("Choisir une image", type=["jpg", "jpeg", "png"])
    col1, col2 = st.columns(2)
    with col1:
        try:
            if img_file is not None:
                img = Image.open(img_file)
                st.image(img, caption="Image choisie",use_container_width=True)
        except Exception as e:
            st.error("Erreur lors du chargement de l'image")
            st.write(e)

    with col2:
        if st.sidebar.button("Détecter"):
            try:
                results = model(img)
                annotated_image = results[0].plot()
                annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

                # Statistiques
                num_objects = len(results[0].boxes)
                detected_classes = [model.names[int(cls)] for cls in results[0].boxes.cls]
                st.write(f"*Nombre d'objets détectés* : {num_objects}")
                st.write(f"*Classes détectées* : {', '.join(detected_classes)}")

                # Affichage de l'image annotée
                st.image(annotated_image_rgb, caption="Objets détectés",use_container_width=True)

                # Téléchargement de l'image annotée
                buf = BytesIO()
                Image.fromarray(annotated_image_rgb).save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(
                    label="Télécharger l'image annotée",
                    data=byte_im,
                    file_name="image_annotated.png",
                    mime="image/png"
                )

            except Exception as e:
                st.error("Erreur lors de la détection")
                st.write(e)

# Détection sur une vidéo
elif input_type == "Vidéo":
    video_file = st.file_uploader("Choisir une vidéo", type=["mp4", "avi", "mov"])
    col1, col2 = st.columns(2)
    with col1:
        try:
            if video_file is not None:
                # Enregistrement temporaire de la vidéo
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                    temp_video.write(video_file.read())
                    video_path = temp_video.name
                # Affichage de la vidéo originale
                st.video(video_path)
        except Exception as e:
            st.error("Erreur lors du chargement de la vidéo")
            st.write(e)

    with col2:
        if st.sidebar.button("Détecter"):
            try:
                cap = cv2.VideoCapture(video_path)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                progress_bar = st.progress(0)  # Barre de progression
                frame_count = 0
                stframe = st.empty()

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        st.warning("Fin de la vidéo.")
                        break

                    # Mise à jour de la barre de progression
                    frame_count += 1
                    progress_bar.progress(frame_count / total_frames)

                    # Détection et affichage
                    results = model(frame)
                    annotated_frame = results[0].plot()
                    annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                    stframe.image(annotated_frame_rgb, caption="Objets détectés")

                cap.release()
                os.unlink(video_path)  # Suppression du fichier temporaire

            except Exception as e:
                st.error("Erreur lors de la détection")
                st.write(e)

# Détection en direct avec la webcam
elif input_type == "Webcam":
    run_webcam = st.sidebar.checkbox("Démarrer la webcam")
    stop_webcam = st.sidebar.button("Arrêter la webcam")
    try:
        if (run_webcam and not stop_webcam) or run_webcam:
            webrtc_streamer(
                key="example_webrtc", 
                video_frame_callback=callback_function,
                mode=WebRtcMode.SENDRECV,
                media_stream_constraints={"video": True, "audio": False},
                server_rtc_configuration={  # Add this line
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                }
            )
        elif stop_webcam:
            st.stop()
    except Exception as e:
        st.error("Erreur lors de la détection")
        st.write(e)
