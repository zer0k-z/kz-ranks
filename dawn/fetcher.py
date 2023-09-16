import requests
import os
import json

def get_all_maps():
    url = "https://dawn.sh/api/kz/maps?limit=1000"
    response = requests.get(url)
    if response.status_code == 200:
        return [map_info['name'] for map_info in response.json() if not (map_info['name'].startswith("skz_") or map_info['name'].startswith("vnl_"))]
    else:
        print(f"Request failed, status {response.status_code}")
        return []

path = 'data-all'
if not os.path.exists(path):
    os.makedirs(path)

for map_name in get_all_maps():
    url_all = f"https://dawn.sh/api/kz/records/top?map={map_name}&stage=0&mode=kzt&limit=75000"
    url_pro = f"https://dawn.sh/api/kz/records/top?map={map_name}&stage=0&mode=kzt&limit=75000&runtype=pro"
    print(f"Fetching {map_name}")
    # Get all PRO runs
    for _ in range(0,5):
        records = []
        response = requests.get(url_pro)
        if response.status_code == 200:
            records = response.json()
            if len(records) == 0:
                break
            file_name = f"{map_name}-PRO.json"
            save_file = open(f"{path}/{file_name}", "w")
            json.dump(records, save_file)
            save_file.close()
            break
        elif response.status_code == 204:
            print(f"No data for {map_name}")
            break
        else:
            print(f"Request failed, status {response.status_code}")
    
    # Get all TP runs
    for _ in range(0,5):
        records = []
        response = requests.get(url_all)
        if response.status_code == 200:
            json_data = response.json() 
            if len(json_data) == 0:
                break
            for record in json_data:
                # Go through the current list, if there's another slower time with the same steam ID then override it. Does nothing if faster.
                # If there's no time with the same steam ID then add it.
                # Note: real slow.
                add = True
                for existing_record in records:
                    if existing_record['steam_id'] == record['steam_id']:
                        add = False
                        if existing_record['time'] > record['time']:
                            records.remove(existing_record)
                            add = True
                if add:
                    records.append(record)
                    
            file_name = f"{map_name}-NUB.json"
            save_file = open(f"{path}/{file_name}", "w")
            json.dump(records, save_file)
            save_file.close()
            break
        elif response.status_code == 204:
            print(f"No data for {map_name}")
            break
        else:
            print(f"Request failed, status {response.status_code}")
    