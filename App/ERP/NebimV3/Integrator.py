import requests

class Integrator:

    url = ""

    payload = {}
    headers = {}

    def __init__(self, url):
        self.url = url

    def get(self, path, headers=None):
        return requests.get(f'{self.url}{path}', headers=headers)

    def post(self, path, data):
        response = requests.post(f'{self.url}{path}', json=data)
        return response

