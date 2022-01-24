import json
from flask import Flask, render_template, \
                  request, redirect, flash, \
                  url_for


def _initialize_clubs():
    data = {'clubs': []}
    with open('clubs.json' , 'w') as club_file:
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

def clubs_with_comp_keys(the_clubs, competitions):
    for c in the_clubs:
        c['reserved_places'] = {}
        for comp in competitions:
            c['reserved_places'][comp['name']] = 0
    return the_clubs


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
only_clubs = loadClubs()
clubs = clubs_with_comp_keys(only_clubs, competitions)

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
        competition_name = the_competition['name']
        already_reserved = the_club['reserved_places'][competition_name]
        placesRequired = int(request.form['places'])
        points_to_substract = 3 * placesRequired
        total_places_reserved = placesRequired + already_reserved
        actual_club_points = int(the_club['points'])
        actual_competition_places = int(the_competition['numberOfPlaces'])
        new_club_points = actual_club_points - points_to_substract
        new_competition_places = actual_competition_places - placesRequired
        if new_competition_places < 0:
                flash("There's not enough places in this competition \n \
                    to book all these places")
                return render_template('welcome.html',
                                       club=the_club,
                                       competitions=competitions)
        elif new_club_points < 0:
            flash("You don't own enough points to book all these places")
            return render_template('booking.html',
                                   club=the_club,
                                   competition=the_competition)
        elif total_places_reserved > 12:
            flash("You can't book more than 12 places for a competition !")
            return render_template('booking.html',
                                   club=the_club,
                                   competition=the_competition)      
        else:
            the_competition['numberOfPlaces'] = str(new_competition_places)
            the_club['points'] = str(new_club_points)
            the_club['reserved_places'][competition_name] = total_places_reserved
            confirm_text = "Great-booking complete! "
            confirm_text += f"You successfully booked {placesRequired} places for the "
            confirm_text += f"competition {competition_name}. You spend {points_to_substract} points."
            flash(confirm_text)
            return render_template('welcome.html',
                                   club=the_club,
                                   competitions=competitions)


@app.route('/showClubsPoints/<club>')
def showClubsPoints(club):
    # club est vide si on vient de l'index /
    # club est le nom du club connecté
    #   si on vient de /showSummary ou de /book/...
    if club == 'offline':
        actual_club = {'name': 'offline'}
        return render_template('dashboard.html',
                                actual_club=actual_club,
                                clubs=clubs)
    else:
        the_club = [c for c in clubs if c['name'] == club]
        if the_club:
            actual_club = the_club[0]
            return render_template('dashboard.html',
                                   actual_club=actual_club,
                                   clubs=clubs)
        else:
            flash("Something went wrong-please try again")
            return redirect(url_for('index'))



@app.route('/logout')
def logout():
    flash('You are now disconnected, thank you for your visit here !')
    return redirect(url_for('index'))
