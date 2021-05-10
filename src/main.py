from cowin_search import CowinApi
import pandas as pd
import json


if __name__ == '__main__':
    api = CowinApi()
    res = api.get_centres_by_state_age_time("Delhi","COVISHIELD", ("07-05-2021","15-05-2021"), 45)
    res = res.to_json()
    data = json.loads(res)
    print(pd.json_normalize(data))

