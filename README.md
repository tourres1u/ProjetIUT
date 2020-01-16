# PT3-Bot-Informatique

Nous sommes sur la version **3.7 de Python**.

Projet Réalisé par :<br/>
Benoît T<br/>
Rova R<br/>
Sebastien B

L’objectif de ce projet est de construire une application, plus spécifiquement un bot.<br/>
Celui-ci surfera indépendamment sur Internet, au sein des réseaux sociaux tels qu'Instagram, Facebook, Twitter et d’autres.<br/>
Sa première mission est de faciliter la vie de l'utilisateur. Pour sa seconde mission, le bot jouera le rôle d'un compagnon, donc l'utilisateur gagnera du temps.<br/>
Concrètement, le bot va :
- Publier automatiquement à une date spécifiée et d'une manière spécifiée.<br/>
- Rechercher des informations et les reprendre dans un tableau de bord<br/>
- Interagir (réponses automatiques, likes, abonnements…)<br/>

Pour tester, c'est simple:

    -Aller dans PT3-Bot-Informatique/v3.0/src/main_pt3/ 
    -puis lancer main.py avec l'environnement de votre choix après avoir réglé les imports et les logiciels à installer.
    -Aller sur localhost sur le port 5000 (127.0.0.1:5000)
    -Les identifiants de connexion sont à me demander en messages privés.

**__TRÈS IMPORTANT__**

**Il faut charger toutes les libraires et les modules avant de pouvoir tester**. (PyTesseract, twilio, etc.)

**Il faut installer manuellement certains package avec pip install. Ex twilio, flask, Tools, pytesseract, etc.**
 
Sur PyCharm, **il faut que les packages src_bot et API_PACKAGE soient dans le path du project interpreter pour la version 3.0**.

**IL FAUT INSTALLER PYTESSERACT** et éventuellement mettre à jour le chemin dans le code (module Twitter_API pour la version 3.0 fonctions getNotifications() et getMentions()). 
Par défaut, le chemin est : **C:/Program Files (x86)/Tesseract-OCR/tesseract**.
Lien pour telecharger l'OCR PyTesseract : https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows



