import requests
import yaml
from getpass import getpass
import os
import json

from EnergyCertificates import Search

CONF_FILE = "config.yml"

class GovApi :
    URI = "https://api.get-energy-performance-data.communities.gov.uk"

    def __init__(self) :
        self.secret = None
        self.get_secret()

    @property
    def config(self) :
        if not os.path.exists(CONF_FILE) : return None
            
        with open(CONF_FILE,'r') as file:
            return yaml.safe_load(file)
    
    @config.setter
    def config(self, value) :
        with open(CONF_FILE,'w') as file:
            yaml.dump({'Auth-Token':value},file)

    def get_secret(self) :
        try :
            self.secret = self.config['Auth-Token']
        except KeyError, TypeError :
            self.secret = getpass("Please enter your Bearer Token: ")
            self.config = self.secret
    
    def get_data(self,path,**kwargs) :
        data = requests.get(GovApi.URI + path, headers= {
            "Authorization": f"Bearer {self.secret}",
            "Accept": "application/json"
        }, params=kwargs)

        self.URL = data.url
        
        if data.status_code != 200 :
            print(data.status_code, data.json()["data"]["error"])
        else :
            print(200)
            return data.json()
            # print(json.dumps(data.json(), indent=2))


if __name__ == "__main__":
    api = GovApi()
    # Working data centre address
    # address = "13 Liverpool Road"

    dataCentre = Search()
    dataCentre.address = "13 Liverpool Road"
    dataCentre.set_date(2018,2018)

    # api.get_data(Search.path,**dataCentre.params)

    beaconsfield = Search()
    beaconsfield.constituency = "Beaconsfield"
    
    # api.get_data(Search.path,**beaconsfield.params)

    old = Search()
    old.set_date(2011,2012)

    data = api.get_data(Search.path,current_page=2,**old.params)
    print(json.dumps(data, indent=2))
    print(api.URL)

    """ Page formating
    "pagination": { 
        "totalRecords": 33306,
        "currentPage": 1,
        "totalPages": 7,
        "nextPage": 2,
        "prevPage": null,
        "pageSize": 5000
    }
    """

    # Is there any older certificates?
    newSearch = Search()
    newSearch.set_date(2010,2013)
    newSearch.constituency = "Beaconsfield"

    data = api.get_data(Search.path,**newSearch.params)
    import pandas as pd # lazy import
    old_data_frame = pd.DataFrame(data['data'])

    old_data_frame.shape # 5000,13 = paginated
    old_data_frame["registrationDate"] = pd.to_datetime(old_data_frame["registrationDate"])

    # If the API pulls more than 5000, the months will sort oldest first
    print("Year count:\n",old_data_frame["registrationDate"].dt.year.value_counts())
    print("Month count:\n",old_data_frame["registrationDate"].dt.month_name().value_counts())


        
