# **Détection d'Objets avec YOLOv5**

## **Description**

Cette application utilise le modèle **YOLOv5** (You Only Look Once) pour détecter des objets dans des images, vidéos ou en direct avec la webcam. Elle est conçue pour être simple, intuitive et accessible via une interface utilisateur développée avec **Streamlit**.

Les principales fonctionnalités incluent :
- Détection d'objets dans des **images**.
- Détection d'objets dans des **vidéos** (frame par frame).
- Détection en temps réel avec la **webcam**.
- Affichage des statistiques (nombre d'objets détectés, classes identifiées).
- Téléchargement des résultats annotés.

---

## **Installation**

### **1. Prérequis**
Assurez-vous que les bibliothèques suivantes sont installées sur votre système :
- Python 3.8 ou supérieur
- OpenCV (`cv2`)
- Streamlit
- Ultralytics YOLOv5
- PIL (Pillow)

Normalement, en installant ultralytics, on a opencv qui s'installe automatiquement.

### **2. Installation des dépendances**

Exécutez la commande suivante pour installer les bibliothèques nécessaires :

```
pip install streamlit ultralytics
```

### **3. Téléchargement du modèle YOLOv5**

Le modèle YOLOv5 doit être téléchargé avant d'exécuter l'application. Placez le fichier du modèle (par exemple, `yolov5su.pt`) dans le même répertoire que votre script principal.

Vous pouvez télécharger un modèle pré-entraîné depuis le dépôt officiel de YOLOv5 :  
https://github.com/ultralytics/yolov5

---

## **Utilisation**

### **1. Lancer l'application**

Pour exécuter l'application, utilisez la commande suivante dans votre terminal :

```
streamlit run yolo_detection_project.py
```

L'application s'ouvrira automatiquement dans votre navigateur web.

---

### **2. Interface utilisateur**

Une fois l'application lancée, vous verrez une interface utilisateur avec les options suivantes :

#### **Barre latérale**

- **Choix du type d'entrée** : Sélectionnez entre "Image", "Vidéo" ou "Webcam".
- **Bouton "Détecter"** : Lance la détection d'objets pour l'entrée sélectionnée.

#### **Sections principales**

- **Image** :
  - Téléchargez une image au format `.jpg`, `.jpeg` ou `.png`.
  - Cliquez sur "Détecter" pour afficher les objets détectés.
  - Téléchargez l'image annotée après la détection.

- **Vidéo** :
  - Téléchargez une vidéo au format `.mp4`, `.avi` ou `.mov`.
  - Cliquez sur "Détecter" pour traiter la vidéo frame par frame.
  - Une barre de progression indique l'avancement du traitement.

- **Webcam** :
  - Activez la webcam en cochant "Démarrer la webcam".
  - La détection se fait en temps réel.
  - Arrêtez la capture en cliquant sur "Arrêter la webcam".

---

## **Fonctionnalités supplémentaires**

### **1. Statistiques**

Après chaque détection, l'application affiche :
- Le nombre total d'objets détectés.
- Les classes d'objets identifiées (par exemple, "personne", "voiture", etc.).

### **2. Téléchargement des résultats**

- Pour les images, vous pouvez télécharger l'image annotée après la détection.
- Pour les vidéos, vous pouvez ajouter une option de téléchargement si nécessaire (non implémentée dans ce code).


---

## **Contributeurs**
- [Votre Nom]  
  Si vous souhaitez contribuer ou signaler des bugs, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

---


---

## **Remerciements**
- **Ultralytics** pour le modèle YOLOv5 : https://github.com/ultralytics/yolov5
- **Streamlit** pour la création de l'interface utilisateur : https://streamlit.io/

---

Avec ce README, vos utilisateurs auront toutes les informations nécessaires pour installer, exécuter et utiliser votre application. 😊
