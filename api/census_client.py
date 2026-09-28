import requests
from dotenv import load_dotenv
import os
load_dotenv()

class CensusClient:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        print('Census client initialized successfully.')

    def get_census_data(self):
        api_variables = 'AGE_DESC,AGECAT,COUNTY,GEOCAT,GEOID,IPR_DESC,IPRCAT,NAME,NIC_LB90,NIC_MOE,NIC_PT,NIC_UB90,NIPR_LB90,NIPR_MOE,NIPR_PT,NIPR_UB90,NUI_LB90,NUI_MOE,NUI_PT,NUI_UB90,PCTIC_LB90,PCTIC_MOE,PCTIC_PT,PCTIC_UB90,PCTUI_LB90,PCTUI_MOE,PCTUI_PT,PCTUI_UB90,RACE_DESC,RACECAT,SEX_DESC,SEXCAT,STABREV,STATE,YEAR'
        time = '2020'
        url = f'http://api.census.gov/data/timeseries/healthins/sahie?get={api_variables}&time={time}&for=state:*&key={self.api_key}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return { 'status_code': response.status_code, 'error': response.text }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Census API: {e}")
            return { 'status_code': None, 'error': str(e) }