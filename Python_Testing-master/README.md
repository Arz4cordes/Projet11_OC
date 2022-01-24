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

3) Environnement virtuel à mettre en place pour utiliser l'application:
    * installer un environnement virtuel Python avec la commande python -m venv envp11
    * activer cet environnement virtuel
        avec la commande envp11/Scripts/activate sous Windows
        ou avec la commande source env/bin/activate sous Mac OS

4) Le fichier requirements.txt contient les bibliothèques à installer:
    utiliser par exemple la commande python -m pip install -r requirements.txt
    pour installer les bibliothèques utilisées dans l'application.

5) Pour utiliser l'application après avoir mis en place l'environnement virtuel
    et installé les bibliothèques:
    * Sous Windows avec Powershell, taper la commande de configuration:
        $env:FLASK_APP = "server.py"
        puis lancer le serveur avec la commande: python -m flask run
    * Sous Mac OS, taper la commande de configuration: export FLASK_APP=server.py
        puis lancer le serveur avec la commande: flask run (ou bien python -m flask run)

6) Après avoir lancé le serveur, entrer l'adresse http://127.0.0.1:5000/ , indiquée par la console,
    dans un navigateur web (Edge, Chrome, Firefox ...)

7) Lorsque le serveur est lancé à l'étape précédente, vous pouvez lancer la série de tests avec la commande:
    pytest 
    (ou bien vous pouvez aussi utiliser pytest -v pour davantage de détails
     ou pytest -s pour afficher éventuelement les print codés dans les fichiers)

     #### Détail des tests ####
     I) Avec la commande pytest, deux tests fonctionnels seront lancés dans le navigateur Chrome.
        Ces tests fonctionnels sont codés dans le fichier tests_use_case.py du dossier functionnal_test.
        Ce dossier contient aussi un sous-dossier chromedriver_windows avec l'éxecutable chromedriver pour windows.
        Si vous êtes sous Mac OS ou Linux, voir le premier point de l'annexe 9 ci-dessous.
        Attention, les deux tests fonctionnels prévoient de réserver un total de 4 places pour le 1er club
        de la liste du json. Le 1er club du json doit donc posséder initialement un total de 12 points au minimum,
        et il faut veiller à couper puis relancer le serveur flask avant de lancer à nouveau des tests fonctionnels,
        sinon les tests fonctionnels échoueront avec des réservations successives.
        Ceci est dû au choix des cas d'usage, non exhaustifs, illustrés par ces tests fonctionnels. 
    II) De plus, 28 tests fonctionnels seront lancés: ils testent chacune des fonctions écrites dans le fichier principal
        server.py
        Important ! Si vous voulez uniquement lancer les tests unitaires, remplacez la commande pytest par la commande
        pytest tests/unit-tests
    III) Un test de performance peut par ailleurs être réalisé avec Locust.
            Pour cela, vous pouvez taper la commande suivante:
            locust -f tests/performance_tests/locustfile.py --csv=tests/performance_tests/rapports_locust  --headless -t10m --users=6 --run-time=10 --host=http://127.0.0.1:5000 --csv-full-history
            Cette commande effectue un test de performance sur l'application dans le cas où 6 utilisateurs sont connectés en même temps, et les rapports
            du test de performance seront écrits dans des fichiers csv situés dans le dossier performance_tests, sous dossier de tests
            Si vous ne souhaitez pas enregistrer les rapports dans un fichier, vous avez aussi la possibilité de lancer la commande suivante:
            locust -f tests/performance_tests/locustfile.py  
            et il faudra alors se rendre à l'adresse http://localhost:8089 dans un navigateur web pour configurer les tests avec locust
            (l'adresse à rentrer dans le champ application est http://127.0.0.1:5000 )
    IV) La couverture de tests peut être exportée dans un fichier html avec la commande: pytest --cov=server.py 
        En ouvrant dans un navigateur web le fichier index.html situé dans le dossier htmlcov, vous pourrez alors
        avoir le détail des fonctions couvertes par les tests.

8) Des captures d'écran de la couverture de tests avant les modifications sur le projet puis après toutes les améliorations et 
    corrections de bug sont visibles dans le dossier captures/ecran_performances_couverture
    Des captures d'écran des tests de performance avec Locust réalisés avant les modifications sur le projet puis après toutes
    les améliorations et corrections de bug sont visibles dans ce même dossier captures/ecran_performances_couverture

9) ANNEXE: liens vers les différentes documentations externes

** Si vous êtes sous Mac OS ou Linux, vous devrez installer ChromeDriver pour mac ou linux
via un téléchargement présent sur cette page:  https://sites.google.com/chromium.org/driver/
La dernière version stable de ChromeDriver est pour Chrome version 97 (vérifier que vous avez cette version de Chrome)
et elle peut être téléchargée sur cette page: https://chromedriver.storage.googleapis.com/index.html?path=97.0.4692.71/
Attention ! Vous devrez placer l'executable ChromeDriver dans le dossier chromedriver_app, sous dossier de tests/functional_tests.
Si le nom de l'éxécutable est différent de 'chromedriver', il faudra alors modifier la variable CD_PATH à la ligne 25 du fichier
test_use_case.py situé dans tests/functionnal-tests pour que chromedriver soit bien trouvé par Selenium.
Enfin, si vous souhaitez utiliser Selenium avec d'autres navigateurs web , rendez vous sur cette page:
https://selenium-python.readthedocs.io/installation.html
(au point 1.5, une liste de liens vers les différents drivers est donnée)

** Documentation de Locust: http://docs.locust.io/en/stable/index.html

** Documentation de Selenium: https://www.selenium.dev/selenium/docs/api/py/api.html

** Pour en savoir davantage sur Flask et sur Pytest, c'est ici:
    https://flask.palletsprojects.com/en/2.0.x/
    https://docs.pytest.org/en/6.2.x/
