# PROJET 11 OC
Correction de bugs, nouvelles fonctionnalités et amélioration des performances,
concernant une application d'inscription à des tournois.

1) Rappel des objectifs de l'application:
    * Seules les secrétaires des clubs ont accès à l'application
    * Les secrétaires doivent se connecter avec leur email pour utiliser l'application
        (hormis pour voir le tableau récaputilatif des points de chaque club)
    * Les secrétaires peuvent se déconnecter après avoir utilisé l'application
    * Chaque club possède un certain nombre de points
        a) Chaque club peut voir son solde actuel de points
        b) Un tableau public en lecture seule permet de voir le nombre de points de chaque club,
            ce tableau est visible hors connection
        c) Chaque club dépense un point lorsqu'il réserve une place pour un de ses athlètes
            à une compétition, sous réserve que cette réservation soit possible
    * Modalités d'inscription à une compétition:
        a) Chaque compétition a un nombre limité d'inscriptions
        b) Chaque club ne peut inscrire qu'un maximum de 12 athlètes,
            dans la limite des places disponibles et du nombre de points restant pour le club
        c) Le nombre de places encore disponible est indiqué lorsqu'une secrétaire est connectée,
            et ce nombre de places est mis à jour après une nouvelle inscription
        d) Un message d'erreur s'affiche si le concours est complet,
            si le club n'a plus suffisamment de points,
            ou si une secrétaire essaie d'inscrire plus de 12 athlètes du club à la compétition
    * Actions possibles pour une secrétaire connectée à l'application:
        a) Lire le solde de points restant pour le club
        b) Lire le solde de points restant pour l'ensemble des clubs (visible hors connection)
        c) Voir l'ensemble des compétitions à venir et sélectionner une des compétitions
        d) Réserver une ou plusieurs places lorsqu'une compétition a été selectionnée
            (des messages d'erreur s'affichent en cas d'impossibilité de réservation)
    * Performances:
        a) Une liste de compétitions doit être affichée en 5 secondes maximum
        b) Une mise à jour du nombre total de points doit être effectuée en 2 secondes maximum
    
2) Pour télécharger l'application, voici le lien GitHub:
    https://github.com/Arz4cordes/Projet11_OC

3) Pour utiliser les programmes:
    * installer un environnement virtuel Python avec la commande python -m venv envp11
    * activer cet environnement virtuel
        avec la commande envp11/Scripts/activate sous Windows
        ou avec la commande source env/bin/activate sous Mac OS

3) Le fichier requirements.txt contient les bibliothèques à installer:
    utiliser par exemple la commande python -m pip install -r requirements.txt
    pour installer les bibliothèques utilisées dans l'application.
        