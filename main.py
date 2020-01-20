from dinnerly import Dinnerly
import pprint
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-u' ,'--username', type=str,
                    help='username for Dinnerly', required=True)

parser.add_argument('-p', '--password', type=str,
                    help='Password for Dinnerly', required=True)

args = parser.parse_args()

username = args.username
password = args.password

dinnerly = Dinnerly(username, password)
dinnerly.login()
recipies = dinnerly.getCurrentRecpies()

recipies = sorted(recipies, key = lambda i: datetime.strptime(i['delivery_date'], "%Y-%m-%d")) 

required = set()

for week in recipies:
    print(week["delivery_date"])
    for recipie in week["recipes"]:
        detail = dinnerly.getDetailedRecipe(recipie["id"])
        for requiredStuff in detail["assumed_ingredients"]:
            required.add(requiredStuff["name"])

pprint.pprint(required)

recipie = dinnerly.getDetailedRecipe(recipies[0]["recipes"][0]["id"])
pprint.pprint(recipie)