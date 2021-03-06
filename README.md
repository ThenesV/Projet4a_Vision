# Projet4a_Vision_Basler_python

Camera Basler aca3088 57uc - USB 3.0

![image](https://user-images.githubusercontent.com/100229511/174100757-797c9316-a6af-4177-adb9-1a84e718b100.png)

Robot Staubli TX90

![image](https://user-images.githubusercontent.com/100229511/174104710-259c454f-7c13-4d78-8790-d2e2d7443e00.png)


# Webcam tests: 

 - test/test_vision_camera.py : détection couleur bleu / objet avec une webcam
 
 - camera_telephone_v1 : détection de couleur avec une interface pour modifier le masque en temps réel (webcam ou téphone avec URL) 
 
# Camera Basler:

 - pylon_camera_serial.py : connecte la caméra à l'ordi (avec numéro de série)
 
 - pylon_multiple_camera.py : connecte la/les caméra(s) à l'ordi (sans numéro de série)

Avant de lancer le code avec la caméra, il faut aller sur le logiciel pylon viewer (avec la caméra) et changer un paramètre (filtre Bayer à BGR):

 - pylon_camera_color.py : détection de couleur (bleu) avec la Caméra Basler
 
 - pylon_camera_color_detection.py : détection de couleur avec une interface pour choisir la couleur (masque) avec la Caméra Basler
 
 ![image](https://user-images.githubusercontent.com/100229511/174100912-911a2bbe-0a46-47bf-87e4-ac10eb0c5f49.png)
 
 - Version finale :  pylon_camera_color_finale.py : détection de couleur avec une interface pour choisir la couleur (masque) et détection de position de la bouteille avec la Caméra Basler

Interface pour choisir la couleur du masque (Teinte, Saturation, Luminance - HSV)

 ![image](https://user-images.githubusercontent.com/100229511/174100324-2c48a0f4-dea4-438c-9d2b-592acc31e3f2.png)
 
 
 
# Protocole :

- Connecter la caméra Basler sur l'ordinateur (USB 3.0)

- Aller sur le logiciel pylon viewer - modifier le paramètre : Image format pour BGR8

![Capture d’écran 2022-06-09 151506](https://user-images.githubusercontent.com/100229511/175516647-34eaccb2-3394-4fd0-b681-76d07bf0b31b.png)

Notre environnement de travail : Visual Studio Code - Anaconda - python

Bibliothèques : OpenCV, pypylon, numpy

- Ouvrir le code : pylon_camera_color_finale.py

- lancer le code




# Environnement SRS

![env](https://user-images.githubusercontent.com/100229511/174104298-46ed8e6c-7b2c-425a-8e97-345e93d59f62.PNG)

