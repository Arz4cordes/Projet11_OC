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
