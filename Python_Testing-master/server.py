import json
from flask import Flask, render_template, \
                  request, redirect, flash, \
                  url_for


def _initialize_clubs():
    data = {'clubs': []}
    with open('clubs.json', 'w') as club_file:
        json.dump(data, club_file, indent=4)
    return []

def loadClubs():
    with open('clubs.json') as c:
        try:
            listOfClubs = json.load(c)['clubs']
            # listOfClubs est une liste de dictionnaires avec les clés name, email, points
            return listOfClubs
        except KeyError:
            c.close()
            listOfClubs = _initialize_clubs()
            return listOfClubs

def _initialize_competitions():
    data = {'competitions': []}
    with open('competitions.json', 'w') as comp_file:
        json.dump(data, comp_file, indent=4)
    return []

def loadCompetitions():
    with open('competitions.json') as comps:
        try:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
        except KeyError:
            comps.close()
            listOfCompetitions = _initialize_competitions()
            return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club == []:
        flash("Sorry, this email doesn't exist in the database...")
        return redirect(url_for('index'))
    else:
        actual_club = club[0]
    return render_template('welcome.html', club=actual_club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']]
    club = [c for c in clubs if c['name'] == request.form['club']]
    if club == [] or competition == []:
        flash("Something went wrong: club does not exist \n \
               or there is no competitions")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        the_competition = competition[0]
        the_club = club[0]
        placesRequired = int(request.form['places'])
        the_competition['numberOfPlaces'] = str(int(the_competition['numberOfPlaces']) - placesRequired)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=the_club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

with app.test_request_context():
    print('#### URL FOR ####')
    print(url_for('index'))
    print(url_for('showSummary'))
