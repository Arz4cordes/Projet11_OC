import json

import pytest
from flask import request

import server
from server import loadClubs, loadCompetitions, index, showSummary, \
                   book, purchasePlaces, logout

"""
Test de la fonction loadClubs:
Verifier que la fonction renvoie bien une liste de clubs
indiquée dans un fichier json
Verifier que la fonction crée une clé Clubs
et renvoie une liste vide
si le fichier json ne contient pas la clé Clubs
"""
class MockResponseClubs:

    @staticmethod
    def load(a_file):
        return {"clubs":[
        {"name": "myclub", "email": "abc@mybox.com", "points": "25"}
    ]}

def test_loadClubs_return_listOfClubs(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponseClubs().load('clubs.json')

    monkeypatch.setattr(json, "load", mock_get)
    expected_value = [
        {"name": "myclub", "email": "abc@mybox.com", "points": "25"}
    ]
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
Test de la fonction loadCompetitions:
Verifier que la fonction renvoie bien une liste de competitions
indiquée dans un fichier json
Verifier que la fonction crée une clé Compétitions
et renvoie une liste vide si le fichier
json ne contient pas la clé Competitions
"""
class MockResponseCompetitions:

    @staticmethod
    def load():
        return {"competitions":[
        {"name": "Legends", "date": "2020-10-22 13:30;00", "numberOfPlaces": "25"}
    ]}

def test_loadCompetitions_return_listOfCompetitions(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponseCompetitions().load()

    monkeypatch.setattr(json, "load", mock_get)
    expected_value = [
        {"name": "Legends", "date": "2020-10-22 13:30;00", "numberOfPlaces": "25"}
    ]
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
Test de la fonction index:
Vérifier que l'accès à la page est OK
Vérifier que la requête post n'est pas permise
Vérifier que la requète http fonctionne avec l'url mentionnée
"""
@pytest.fixture
def client():
    new_app = server.app
    new_app.testing = True
    with new_app.test_client() as c:
        yield c

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
