import json
from flask import Flask, render_template, \
                  request, redirect, flash, \
                  url_for


def _initialize_clubs():
    data = {'clubs': []}
    with open(clubs_file, 'w') as club_file:
        json.dump(data, club_file, indent=4)
    return []


def loadClubs():
    with open(clubs_file) as c:
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
    with open(competitions_file, 'w') as comp_file:
        json.dump(data, comp_file, indent=4)
    return []


def loadCompetitions():
    with open(competitions_file) as comps:
        try:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
        except KeyError:
            comps.close()
            listOfCompetitions = _initialize_competitions()
            return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'
competitions_file = 'competitions.json'
clubs_file = 'clubs.json'
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
        return render_template('booking.html', club=foundClub[0], competition=foundCompetition[0])
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
        new_club_points = int(the_club['points']) - placesRequired
        if placesRequired > 12:
            flash("You can't book more than 12 places for a competition !")
            return render_template('booking.html', club=the_club, competition=the_competition)
        elif new_club_points < 0:
            flash("You don't own enough points to book all these places")
            return render_template('booking.html', club=the_club, competition=the_competition)
        else:
            new_competition_points = int(the_competition['numberOfPlaces']) - placesRequired
            if new_competition_points < 0:
                flash("There's not enough places in this competition \n \
                    to book all these places")
                return render_template('booking.html', club=the_club, competition=the_competition)
            else:
                the_competition['numberOfPlaces'] = str(new_competition_points)
                the_club['points'] = str(new_club_points)
                flash('Great-booking complete!')
                return render_template('welcome.html', club=the_club, competitions=competitions)


@app.route('/showClubsPoints/<club>')
def showClubsPoints(club):
    # club est vide si on vient de l'index /
    # club est le nom du club connecté
    #   si on vient de /showSummary ou de /book/...
    the_club = [c for c in clubs if c['name'] == club]
    if the_club:
        actual_club = the_club[0]
    else:
        actual_club = ""
    return render_template('dashboard.html',
                            actual_club=actual_club,
                            competitions=competitions,
                            clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
