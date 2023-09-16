import json
import os
import scipy.stats as stats
import argparse
import time
from map_rank_proposal_point_calc import *
from map_rank_proposal_helper import *


def read_json_file(file_path, pro = False):
    path = "maptops"
    if pro:
        path = "maptops-pro"
    try:
        with open(f"{path}/{file_path}.json", "r", encoding= 'utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def parse_file(file_path):
    # NUB leaderboard
    start_time = time.time()
    json_data_nub = read_json_file(file_path, False)
    if json_data_nub:
        print(f"[NUB] Records count: {len(json_data_nub)}")
        json_data_nub = sorted(json_data_nub, key=lambda x: x["time"])
        times_nub = np.array([data['time'] for data in json_data_nub])
        print([data['time'] for data in json_data_nub])
        exit()
        # Make a curve out of the data
        norminvgauss_params_nub = stats.norminvgauss.fit(times_nub)
        norminvgauss_dist_nub = stats.norminvgauss(*norminvgauss_params_nub)

        sanitized_names = [sanitize_name_md(data['player_name']) for data in json_data_nub]
        dist_wr_sf_nub = 1 - norminvgauss_dist_nub.cdf(times_nub[0])
        num_times_nub = len(json_data_nub)
        for i, data in enumerate(json_data_nub):
            data['points'] = get_points(norminvgauss_dist_nub, data['time'], times_nub[0], json_data_nub[0]['stage_tier'], i, num_times_nub, False, dist_wr_sf_nub)

        if not os.path.exists("maptop-proposal"):
            os.makedirs("maptop-proposal")
        with open(f"maptop-proposal/{file_path}-NUB.json", "w") as json_file:
            json.dump(json_data_nub, json_file)
        new_points = [[i+1, sanitized_names[i], format_seconds(data['time']), data['points']] for i, data in enumerate(json_data_nub)]

        table = [["#", "Name", "Time", "Points"]] + new_points

        if not os.path.exists("tables"):
            os.makedirs("tables")
        with open(f"tables/{file_path}-NUB.md", "w", encoding="utf-8") as file:
            file.write(make_markdown_table(f"{file_path} (NUB)", table))
        print(f"[NUB] Parsing took {time.time() - start_time}")
        start_time = time.time()
    else:
        return
    # PRO leaderboard
    json_data_pro = read_json_file(file_path, True)

    if json_data_pro:
        print(f"[PRO] Records count: {len(json_data_pro)}")
        json_data_pro = sorted(json_data_pro, key=lambda x: x["time"])
        times_pro = np.array([data['time'] for data in json_data_pro])

        # Make a curve out of the data
        norminvgauss_params_pro = stats.norminvgauss.fit(times_pro)
        norminvgauss_dist_pro = stats.norminvgauss(*norminvgauss_params_pro)

        sanitized_names = [sanitize_name_md(data['player_name']) for data in json_data_pro]
        dist_wr_sf_pro = 1 - norminvgauss_dist_pro.cdf(times_pro[0])
        num_times_pro = len(json_data_pro)
        for i, data in enumerate(json_data_pro):
            data['points'] = max(get_points(norminvgauss_dist_pro, data['time'], times_pro[0], json_data_pro[0]['stage_tier'], i, num_times_pro, True, dist_wr_sf_pro),
                                 get_points(norminvgauss_dist_nub, data['time'], times_nub[0], json_data_pro[0]['stage_tier'], np.searchsorted(times_nub, data['time'], side = 'left'), num_times_nub, False, dist_wr_sf_nub))

        with open(f"maptop-proposal/{file_path}-PRO.json", "w") as json_file:
            json.dump(json_data_pro, json_file)

        new_points = [[i+1, sanitized_names[i], format_seconds(data['time']), data['points']] for i, data in enumerate(json_data_pro)]

        table = [["#", "Name", "Time", "Points"]] + new_points

        with open(f"tables/{file_path}-PRO.md", "w", encoding="utf-8") as file:
            file.write(make_markdown_table(f"{file_path} (PRO)", table))

        print(f"[PRO] Parsing took {time.time() - start_time}")

def main():
    path = "maptops"

    # Get a list of file names in the directory
    file_names = os.listdir(path)

    # Remove the suffix from each file name
    file_names_without_suffix = ['bkz_chillhop_go'] #[os.path.splitext(file_name)[0] for file_name in file_names]
    for file_path in file_names_without_suffix:
        print(f"Parsing {file_path}")
        parse_file(file_path)
if __name__ == "__main__":
    main()