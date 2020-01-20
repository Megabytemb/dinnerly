from dinnerly import Dinnerly
import pprint
import argparse

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

recipie = dinnerly.getDetailedRecipe(recipies[0]["recipes"][0]["id"])
pprint.pprint(recipie)