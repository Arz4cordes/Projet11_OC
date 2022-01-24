from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    """
    Tests de performance:
    1. page login
    2. page du menu une fois connecté
    3. page des réservations à partir du menu
    4. retour page du menu après une réservation
    5. déconnection
    6. visualiser la page des points en étant connecté
    Objectifs:
    # Affichage de la page en 2s maximum, avec 6 utilisateurs simultanés
    # Mise à jour des points clubs et compétitions en moins de 5s
        (voir cas numéeo 4)
    """

    @task
    def login_page(self):
        with self.client.get("/",
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Request took too long...")

    @task(3)
    def home_page(self):
        form = {'email': "john@simplylift.co"}
        with self.client.post('/showSummary',
                              data=form,
                              catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Request took too long...")

    @task(2)
    def booking_page(self):
        with self.client.get('/book/"Spring Festival"/"Simply Lift"',
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Request took too long...")

    @task(2)
    def home_page_after_booking(self):
        form = {'club': "Simply Lift",
                'competition': "Spring Festival",
                'places': 5}
        with self.client.post('/purchasePlaces',
                              data=form,
                              catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Request took too long...")

    @task
    def logout_page(self):
        with self.client.get('/logout', catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Request took too long...")

    @task(2)
    def points_dashboard(self):
        with self.client.get('/showClubsPoints/"Simply Lift"',
                             catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Request took too long...")
