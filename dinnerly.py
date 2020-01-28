import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from datetime import timedelta
from datetime import datetime

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
        self.user = self.getUser()

        return

    def _get(self, url):

        headers = {
            "authorization": f"Bearer {self.apiKey}"
        }

        return self.session.get(url, headers=headers)
    
    def getUser(self):
        url = f"https://api.dinnerly.com/users/{self.userId}?brand=dn&country=au&product_type=web"
        
        r = self._get(url)

        return r.json()
    
    def getCurrentRecpies(self):
        url = f"https://api.dinnerly.com/users/{self.userId}/orders/current?brand=dn&country=au&product_type=web"

        r = self._get(url)

        return r.json()
    
    def getThisWeeksRecpies(self):
        recipies = self.getCurrentRecpies()

        # Sort recipies by date
        recipies = sorted(recipies, key = lambda i: datetime.strptime(i['delivery_date'], "%Y-%m-%d")) 

        # remove any recipies from before this weeks's run
        today = date.today()

        deliveryDay = self.user["plan"]["wday"]

        # python starts from 0 for days of the week
        deliveryDay = deliveryDay - 1 % 7

        offset = (today.weekday() - deliveryDay) % 7
        mostRecentDeliveryDate = today - timedelta(days=offset)
        print (mostRecentDeliveryDate)


        for recipie in recipies:
            recipieWeek = datetime.strptime(recipie['delivery_date'], "%Y-%m-%d").date()
            if recipieWeek == mostRecentDeliveryDate:
                return recipie

    
    def getDetailedRecipe(self, recipeId):
        url = f"https://api.dinnerly.com/recipes/{recipeId}?brand=dn&country=au&product_type=web"

        r = self._get(url)

        return r.json()