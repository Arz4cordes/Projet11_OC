import json

import server
from server import loadClubs, loadCompetitions, index, showSummary, \
                   book, purchasePlaces, logout

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

class MockResponseCompetitions:

    @staticmethod
    def load(a_file):
        return {"competitions":[
        {"name": "Legends", "date": "2020-10-22 13:30;00", "numberOfPlaces": "25"}
    ]}

def test_loadCompetitions_return_listOfCompetitions(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponseCompetitions().load('competitions.json')

    monkeypatch.setattr(json, "load", mock_get)
    expected_value = [
        {"name": "Legends", "date": "2020-10-22 13:30;00", "numberOfPlaces": "25"}
    ]
    assert loadCompetitions() == expected_value

class MockResponseEmptyJsonFile:

    @staticmethod
    def load(a_file):
        return {"competitions":[]}

def test_loadCompetitions_with_empty_file(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponseEmptyJsonFile().load('competitions.json')

    def mockreturn():
        data = {'competitions': []}
        with open('file_for_test.json', 'w') as comp_file:
            json.dump(data, comp_file, indent=4)
        with open('file_for_test.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions

    monkeypatch.setattr(json, "load", mock_get)
    monkeypatch.setattr(server, "_initialize_competitions", mockreturn)
    expected_value = []
    assert loadCompetitions() == expected_value
