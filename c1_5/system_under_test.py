import requests


# some code to be tested
class SystemUnderTest:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_data(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
