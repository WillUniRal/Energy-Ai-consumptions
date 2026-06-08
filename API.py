import requests
import yaml
from getpass import getpass
import os

CONF_FILE = "config.yml"

class GovApi :
    URI = "https://api.get-energy-performance-data.communities.gov.uk"

    def __init__(self):
        self.secret = None

    @property
    def config(self) :
        if not os.path.exists(CONF_FILE) : return None
            
        with open(CONF_FILE,'r') as file:
            return yaml.safe_load(file)
    
    @config.setter
    def config(self, value) :
        with open(CONF_FILE,'w') as file:
            yaml.dump({'Auth-Token':value},file)

    def get_secret(self):
        try :
            self.secret = self.config['Auth-Token']
        except KeyError, TypeError :
            self.secret = getpass("Please enter your API Secret: ")
            self.config = self.secret

if __name__ == "__main__":
    api = GovApi()
    
    api.get_secret()

    print(api.secret)
        
