import requests
from bs4 import BeautifulSoup
import re

class Dinnerly():

    host = "https://dinnerly.com.au"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

    def getAuthenticityToken(self):
        r = self.session.get("https://dinnerly.com.au/login")
        soup = BeautifulSoup(r.text, 'html.parser')
        value = soup.find('input', {'name': 'authenticity_token'}).get('value')
        return value
    
    def login(self):
        uri = "/login"

        body = {
            "spree_user[email]": self.username,
            "spree_user[password]": self.password,
            "spree_user[brand]": "dn",
            "authenticity_token": self.getAuthenticityToken()
        }
        r = self.session.post(self.host + uri, body)

        api_key_re = re.compile(r'gon\.api_token="(.+?)";')
        result = api_key_re.search(r.text)
        self.apiKey = result.group(1)

        user_id_re = re.compile(r'gon\.current_user_id=(.+?);')
        result = user_id_re.search(r.text)
        self.userId = result.group(1)

        return

    def _get(self, url):

        headers = {
            "authorization": f"Bearer {self.apiKey}"
        }

        return self.session.get(url, headers=headers)
    
    def getCurrentRecpies(self):
        url = f"https://api.dinnerly.com/users/{self.userId}/orders/current?brand=dn&country=au&product_type=web"

        r = self._get(url)

        return r.json()
    
    def getDetailedRecipe(self, recipeId):
        url = f"https://api.dinnerly.com/recipes/{recipeId}?brand=dn&country=au&product_type=web"

        r = self._get(url)

        return r.json()