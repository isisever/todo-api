import requests

class PassgageAPI:

    url = ""

    payload = {}
    headers = {}

    def __init__(self, url):
        self.url = url

    def get(self, path, headers=None):
        return requests.get(f'{self.url}{path}', headers=headers)

    def post(self, path, headers=None, data=None):
        return requests.post(f'{self.url}{path}', headers=headers, data=data)
