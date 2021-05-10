import requests
import numpy as np
import pandas as pd


class CowinApi:
    def __init__(self):
        self.base_url = "https://cdn-api.co-vin.in/api"
        self.session = requests.Session()
        self.session.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",})

    def get_state_id(self, state_name):
        states = self.session.get(str(self.base_url + '/v2/admin/location/states')).json()
        state_df = pd.DataFrame(states['states'])
        self.state_df = state_df
        return state_df[state_df['state_name'] == state_name]['state_id'].values[0]

    def get_districts(self, state_id):
        districts = self.session.get(str(self.base_url + f'/v2/admin/location/districts/{state_id}')).json()
        dist_df = pd.DataFrame(districts['districts'])
        return dist_df

    def get_centres(self, state_name, district_name, vaccine_name, date, age=45):
        state_id = self.get_state_id(state_name)
        districts = self.get_districts(state_id)
        # print(districts)
        district_id = districts[districts['district_name'] == district_name].district_id
        results = []
        # print(district_id)
        params = {
            "Accept-Langauge": "en_US",
            "district_id": district_id,
            "date": date
        }
        results.append(self.session.get(str(self.base_url + '/v2/appointment/sessions/public/findByDistrict'),
                                        params=params).json())
        centres = []
        for sessions in results[0]['sessions']:
            if vaccine_name != '':
                if sessions['vaccine'] == vaccine_name and sessions['min_age_limit'] == age:
                    centres.append(sessions)
            else:
                centres.append(sessions)
        return pd.DataFrame(centres)

    def get_centres_by_state(self, state_name, vaccine_name, date, age=45):
        state_id = self.get_state_id(state_name)
        dist_df = self.get_districts(state_id)
        results = {}
        for _, row in dist_df.iterrows():
            params = {
                "Accept-Langauge": "en_US",
                "district_id": row.district_id,
                "date": date
            }
            results[row.district_name] = self.session.get(
                str(self.base_url + '/v2/appointment/sessions/public/findByDistrict'), params=params).json()
        centres = []
        for district_name, sessions in results.items():
            list_sessions = sessions['sessions']
            for center in list_sessions:
                # print(center['vaccine'])
                if center['vaccine'] == vaccine_name and center['min_age_limit'] == age:
                    centres.append(center)
        return pd.DataFrame(centres)

    def get_centres_by_state_age(self, state_name, vaccine_name, date, age):
        state_id = self.get_state_id(state_name)
        districts = self.get_districts(state_id)
        results = {}
        for _, row in districts.iterrows():
            # print(row.district_id)
            params = {
                "Accept-Langauge": "en_US",
                "district_id": row.district_id,
                "date": date
            }
            results[row.district_name] = self.session.get(
                str(self.base_url + '/v2/appointment/sessions/public/findByDistrict'), params=params).json()
        centres = []
        for district_name, sessions in results.items():
            list_sessions = sessions['sessions']
            for center in list_sessions:
                if center['vaccine'] == vaccine_name and center['min_age_limit'] == age:
                    centres.append(center)
        return pd.DataFrame(centres)

    def get_centres_by_state_age_time(self, state_name, vaccine_name, date_range, age):
        state_id = self.get_state_id(state_name)
        districts = self.get_districts(state_id)
        results = {}
        start_date = pd.to_datetime(date_range[0], format="%d-%m-%Y")
        end_date = pd.to_datetime(date_range[1], format="%d-%m-%Y")
        dates = pd.to_datetime(np.linspace(start_date.value, end_date.value, abs((end_date - start_date).days)))
        center_dfs = []
        for date in dates:
            for _, row in districts.iterrows():
                params = {
                    "Accept-Langauge": "en_US",
                    "district_id": row.district_id,
                    "date": date.strftime("%d-%m-%Y")
                }
                results[row.district_name] = self.session.get(
                    str(self.base_url + '/v2/appointment/sessions/public/findByDistrict'), params=params).json()
            centres = []
            for district_name, sessions in results.items():
                list_sessions = sessions['sessions']
                for center in list_sessions:
                    if center['vaccine'] == vaccine_name and center['min_age_limit'] == age:
                        centres.append(center)
            center_dfs.append(pd.DataFrame(centres))
        results = pd.concat(center_dfs, ignore_index=True)
        return results

    def get_centres_by_district(self, state_name, district_name, date, vaccine_name, age):
        state_id = self.get_state_id(state_name)
        districts = self.get_districts(state_id)
        # print(districts)
        district_id = districts[districts['district_name'] == district_name].district_id
        params = {
            "Accept-Langauge": "en_US",
            "district_id": district_id,
            "date": date
        }
        results = [self.session.get(str(self.base_url + '/v2/appointment/sessions/public/findByDistrict'),
                                    params=params).json()]
        centres = []
        for sessions in results[0]['sessions']:
            if vaccine_name != '':
                if sessions['vaccine'] == vaccine_name and sessions['min_age_limit'] == age:
                    centres.append(sessions)
            else:
                centres.append(sessions)
        return pd.DataFrame(centres)
