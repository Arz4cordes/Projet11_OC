from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    @task
    def login_page(self):
        self.client.get("/")

    @task(2)
    def home_page(self):
        form = {'email': "john@simplylift.co"}
        response = self.client.post('/showSummary', data=form)

    @task(3)
    def booking_page(self):
        self.client.get('/book/"Spring Festival"/"Simply Lift"')
