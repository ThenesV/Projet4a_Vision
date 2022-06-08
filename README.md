# Projet4a_Vision

Basler caméra - USB 3.0

Webcam:
test/test_vision_camera.py : détection couleur bleu / objet avec une webcam
 
 
Camera Basler:
pylon_camera_serial.py : connecte la caméra à l'ordi (avec numéro de série)
pylon_multiple_camera.py : connecte la/les caméra(s) à l'ordi (sans numéro de série)

Avant de lancer le code avec la caméra, il faut aller sur le logiciel pylon viewer (avec la caméra) et changer un paramètre (filtre Bayer à BGR):
pylon_camera_color.py : détection de couleur (bleu) avec la Caméra Basler

