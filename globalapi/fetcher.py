import requests
import os
import json
MAPS_TP = [
    "kz_kiwipsychosis",
    "kz_portalclimb",
]

MAPS_PRO = [
    "kz_slide_isnt_kz",
    "kz_burnished"
]
def get_player_records(map_name, pro):
    print(f"Fetching {map_name}")
    if pro:
        teleport_string = "false"
        title_pro_string = "PRO"
    else:
        teleport_string = "true"
        title_pro_string = "TP"

    url = f"https://kztimerglobal.com/api/v2/records/top?map_name={map_name}&tickrate=128&has_teleports={teleport_string}&stage=0&modes_list_string=kz_timer&limit=40000"   
    
    for _ in range(0,5):
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            file_name = f"{map_name}-{title_pro_string}.json"
            path = 'data'
            if not os.path.exists(path):
                os.makedirs(path)
            save_file = open(f"{path}/{file_name}", "w")
            json.dump(json_data, save_file)
            save_file.close()
            break
        else:
            print(f"Request failed, status {response.status_code}")
        
for map in MAPS_PRO:
    get_player_records(map, True)

for map in MAPS_TP:
    get_player_records(map, False)
