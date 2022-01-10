import json

import pytest
from flask import request, url_for

import server
from server import loadClubs, loadCompetitions, index, showSummary, \
                   book, purchasePlaces, logout

@pytest.fixture
def list_of_clubs_file():
    # Renvoie un dictionnaire avec la clé 'clubs'
    # correspondant au contenu du fichier json
    the_clubs = {
        "clubs":[
            {
                "name": "myclub",
                "email": "abc@mybox.com",
                "points": "25"
            },
            {
                "name": "otherclub",
                "email": "xyz@mybox.fr",
                "points": "3"
            }
        ]
    }
    return the_clubs

@pytest.fixture
def list_of_competitions_file():
    # Renvoie un dictionnaire avec la clé 'competitions'
    # correspondant au contenu du fichier json
    the_competitions = {
        "competitions":[
            {
                "name": "allStars",
                "date": "2021-03-21 20:30:00",
                "numberOfPlaces": "48"
            },
            {
                "name": "juniorsChampionship",
                "date": "2021-10-22 14:00:00",
                "numberOfPlaces": "10"
            }
        ]
    }
    return the_competitions

@pytest.fixture
def client():
    new_app = server.app
    new_app.testing = True
    with new_app.test_client() as c:
        yield c

"""
TEST DE LA FONCTION loadClubs:
Verifier que la fonction renvoie bien une liste de clubs
indiquée dans un fichier json
Verifier que la fonction crée une clé Clubs
et renvoie une liste vide
si le fichier json ne contient pas la clé Clubs
"""
class MockResponseClubs:

    @staticmethod
    def load(list_of_clubs_file):
        return list_of_clubs_file

def test_loadClubs_return_listOfClubs(monkeypatch, list_of_clubs_file):

    def mock_get(*args, **kwargs):
        return MockResponseClubs().load(list_of_clubs_file)

    monkeypatch.setattr(json, "load", mock_get)
    expected_value = list_of_clubs_file["clubs"]
    assert loadClubs() == expected_value

class MockresponseEmptyClubJsonFile:

    @staticmethod
    def load():
        return {}

def test_loadClubs_with_empty_file(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockresponseEmptyClubJsonFile().load()

    def mockreturn():
        return []

    monkeypatch.setattr(json, "load", mock_get)
    monkeypatch.setattr(server, "_initialize_clubs", mockreturn)
    expected_value = []
    assert loadClubs() == expected_value

"""
TEST DE LA FONCTION loadCompetitions:
Verifier que la fonction renvoie bien une liste de competitions
indiquée dans un fichier json
Verifier que la fonction crée une clé Compétitions
et renvoie une liste vide si le fichier
json ne contient pas la clé Competitions
"""
class MockResponseCompetitions:

    @staticmethod
    def load(list_of_competitions_file):
        return list_of_competitions_file

def test_loadCompetitions_return_listOfCompetitions(monkeypatch, list_of_competitions_file):

    def mock_get(*args, **kwargs):
        return MockResponseCompetitions().load(list_of_competitions_file)

    monkeypatch.setattr(json, "load", mock_get)
    expected_value = list_of_competitions_file['competitions']
    assert loadCompetitions() == expected_value

class MockResponseEmptyCompJsonFile:

    @staticmethod
    def load():
        return {}

def test_loadCompetitions_with_empty_file(monkeypatch):

    def mock_get(fake_data, *args, **kwargs):
        return MockResponseEmptyCompJsonFile().load()

    def mockreturn():
        return []

    monkeypatch.setattr(json, "load", mock_get)
    monkeypatch.setattr(server, "_initialize_competitions", mockreturn)
    expected_value = []
    assert loadCompetitions() == expected_value

"""
TEST DE LA FONCTION index:
Vérifier que l'accès à la page est OK
Vérifier que la requête post n'est pas permise
Vérifier que la requète http fonctionne avec l'url mentionnée
"""

def test_index_status(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_wrong_method(client):
    response = client.post('/')
    assert response.status_code == 405

def test_index_context():
    the_app = server.app
    the_app.testing = True
    with the_app.test_request_context('/'):
        assert request.path == '/'

"""
TEST DE LA FONCTION showSummary:
Vérifier que l'accès à la page est OK avec un club connecté,
vérifier que les arguments club et competitions sont passés à la vue
Vérifier que l'accès à la vue n'est pas permis
si un email incorrect est entré
Vérifier que la page n'est pas accessible avec une méthode get
"""

def test_showSummary_status(mocker, client, list_of_clubs_file):
    existing_club = list_of_clubs_file['clubs'][0]
    correct_email = existing_club['email']
    mocker.patch.object(server, 'clubs', list_of_clubs_file['clubs'])
    form = {'email': correct_email}
    response = client.post('/showSummary',
                           data=form)
    assert response.status_code == 200

def test_showSummary_return_parameters(mocker,
                                       client,
                                       list_of_clubs_file,
                                       list_of_competitions_file):
    
    def mockreturn(list_of_clubs_file, list_of_competitions_file):
        the_club = list_of_clubs_file['clubs'][0]
        the_competitions = list_of_competitions_file['competitions']
        parameters = {
            'club': the_club,
            'competitions': the_competitions
        }
        return parameters
    
    existing_club = list_of_clubs_file['clubs'][0]
    correct_email = existing_club['email']
    mocker.patch.object(server, 'clubs', list_of_clubs_file['clubs'])
    mocker.patch.object(server, 'competitions', list_of_competitions_file['competitions'])
    mocker.patch('server.render_template',
                 return_value=mockreturn(list_of_clubs_file,
                                         list_of_competitions_file))
    form = {'email': correct_email}
    response = client.post('/showSummary',
                           data=form)
    expected_value = {
        'club': existing_club,
        'competitions': list_of_competitions_file['competitions']
    }
    assert showSummary() == expected_value

def test_showSummary_club_not_exists(mocker, client, list_of_clubs_file):
    mocker.patch.object(server, 'clubs', list_of_clubs_file['clubs'])
    form = {'email': 'not_in_clubs@mail.com'}
    response = client.post('/showSummary',
                           data=form)
    print(response.status_code)
    assert response.status_code >= 300

def test_showSummary_wrong_method(mocker, client, list_of_clubs_file):
    mocker.patch.object(server, 'clubs', list_of_clubs_file['clubs'])
    response = client.get('/showSummary')
    assert response.status_code == 405

"""
TEST DE LA FONCTION book:
(competition et club sont passés en paramètres
depuis le template welcome.html lors du click
sur une compétition)
foundClub récupère le club passé en paramètre
foundCompetition récupère la compétition
return: le template booking.html avec
        les paramètres club et competition
ou bien retourne à welcome.html
    si club is None ou competition is None
Tester si la requète http get fonctionne bien
Vérifier que la requète post n'est pas possible
Verifier que les paramètres club et competition
sont bien envoyés au template
Tester le cas où foundcompetition est une liste vide
Tester le cas où foundClubs est une liste vide
Tester la fonction avec des paramètres club et competition
invalides
"""

def test_book_status(client, mocker,
                     list_of_clubs_file,
                     list_of_competitions_file):
    # club est le club actuel
    # competition est la competition choisie
    # clubs est l'ensemble des clubs
    # competitions est l'ensemble des compétitions
    actual_club = list_of_clubs_file['clubs'][0]
    competition_choose = list_of_competitions_file['competitions'][0]
    club = actual_club["name"]
    competition = competition_choose["name"]
    mocker.patch.object(server, 'clubs',
                        list_of_clubs_file['clubs'])
    mocker.patch.object(server, 'competitions',
                        list_of_competitions_file['competitions'])
    book_url = '/book/' + str(competition) + '/' + str(club)
    response = client.get(book_url)
    assert response.status_code == 200

def test_book_wrong_method(client,
                     list_of_clubs_file,
                     list_of_competitions_file):
    actual_club = list_of_clubs_file['clubs'][0]
    competition_choose = list_of_competitions_file['competitions'][0]
    club = actual_club["name"]
    competition = competition_choose["name"]
    book_url = '/book/' + str(competition) + '/' + str(club)
    response = client.post(book_url)
    assert response.status_code == 405

"""
Première version du test concernant les paramètres
renvoyés au template, test à supprimer.
def test_book_return_parameters(client, mocker,
                                list_of_clubs_file,
                                list_of_competitions_file):

    def mockreturn(list_of_clubs_file, list_of_competitions_file):
        the_club = list_of_clubs_file['clubs'][0]
        the_competition = list_of_competitions_file['competitions'][0]
        parameters = {
            'club': the_club,
            'competition': the_competition
        }
        return parameters
    
    # Récupérer le club et la competition
    # passés en paramètres de la fonction
    actual_club = list_of_clubs_file['clubs'][0]
    competition_choose = list_of_competitions_file['competitions'][0]
    club = actual_club["name"]
    competition = competition_choose["name"]
    # mocks pour pouvoir tester la fonction book
    mocker.patch.object(server, 'clubs', list_of_clubs_file['clubs'])
    mocker.patch.object(server, 'competitions', list_of_competitions_file['competitions'])
    mocker.patch('server.render_template',
    return_value=mockreturn(list_of_clubs_file,
                            list_of_competitions_file))
    book_url = '/book/' + str(competition) + '/' + str(club)
    response = client.get(book_url)
    expected_value = {
        'club': actual_club,
        'competition': competition_choose
    }
    assert book(club, competition) == expected_value
    """

def test_book_with_clubs_empty(client, mocker,
                               list_of_clubs_file,
                               list_of_competitions_file):
    actual_club = list_of_clubs_file['clubs'][0]
    competition_choose = list_of_competitions_file['competitions'][0]
    club = actual_club["name"]
    competition = competition_choose["name"]
    mocker.patch.object(server, 'clubs', [])
    mocker.patch.object(server, 'competitions',
                        list_of_competitions_file['competitions'])
    book_url = '/book/' + str(competition) + '/' + str(club)
    response = client.get(book_url)
    assert response.status_code == 200

def test_book_with_competitions_empty(client, mocker,
                               list_of_clubs_file,
                               list_of_competitions_file):
    actual_club = list_of_clubs_file['clubs'][0]
    competition_choose = list_of_competitions_file['competitions'][0]
    club = actual_club["name"]
    competition = competition_choose["name"]
    mocker.patch.object(server, 'clubs', 
                        list_of_clubs_file['clubs'])
    mocker.patch.object(server, 'competitions', [])
    book_url = '/book/' + str(competition) + '/' + str(club)
    response = client.get(book_url)
    assert response.status_code == 200


def test_book_club_not_exists(client, mocker,
                     list_of_clubs_file,
                     list_of_competitions_file):
    club = "fake_club"
    competition = "fake competition"
    mocker.patch.object(server, 'clubs',
                        list_of_clubs_file['clubs'])
    mocker.patch.object(server, 'competitions',
                        list_of_competitions_file['competitions'])
    book_url = '/book/' + str(competition) + '/' + str(club)
    response = client.get(book_url)
    assert response.status_code == 200


from flask import template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    recorded = []
    def record(app, template, context, **extra):
        recorded.append((template, context))
        print(app)
        print("TEMPLATE, CONTEXT")
        print(recorded)
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

def test_template_index(mocker, client,
                        list_of_clubs_file,
                        list_of_competitions_file):
    with captured_templates(server.app) as templates:
        actual_club = list_of_clubs_file['clubs'][0]
        competition_choose = list_of_competitions_file['competitions'][0]
        club = actual_club["name"]
        competition = competition_choose["name"]
        mocker.patch.object(server, 'clubs',
                            list_of_clubs_file['clubs'])
        mocker.patch.object(server, 'competitions',
                            list_of_competitions_file['competitions'])
        book_url = '/book/' + str(competition) + '/' + str(club)
        response = client.get(book_url)
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'booking.html'
        assert context['club'] == [actual_club]
        assert context['competition'] == [competition_choose]
