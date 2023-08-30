# KZ map points calculator for current system
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import statistics
import math

path = 'data'
output_path = 'graphs'
for filename in os.listdir(path):
    if filename.endswith('.json'):
        map_info = filename.removesuffix('.json').split('-')
        map_name = map_info[0]
        pro = map_info[1] == "PRO"
        
        file_path = os.path.join(path, filename)

        with open(file_path, 'r') as json_file:
            
            print(f"-----------")
            print(f"Loading {map_name}({map_info[1]})")
            data = json.load(json_file)
            if len(data) == 0:
                continue
            data[0]['points'] -= 200
            # Remove rank-based rewards
            for i in range(1,len(data)):
                rankfactor = 198 - i * 2
                if rankfactor < 0: rankfactor = 0
                data[i]['points'] -= rankfactor
            records = [(record['time'], record['points']) for record in data]
            points = np.array([record['points'] for record in data])
            
            times = np.array([(record['time']) for record in data])
            print(f"WR: {data[0]['time']} - {data[0]['points']}")
            if len(data) > 20:
                print(f"#20: {data[20]['time']} - {data[20]['points']}")
            if len(data) > 100:
                print(f"#100: {data[100]['time']} - {data[100]['points']}")
            print(f"Threshold for top 75% / 50% / 25% / 10% / 1%: {np.percentile(times, 75)} / {np.percentile(times, 50)} / {np.percentile(times, 25)} / {np.percentile(times, 10)} / {np.percentile(times, 1)}")
            print("Times:", stats.describe(times), "Median:", statistics.median(times),)
            print("Points:", stats.describe(points), "Median:", statistics.median(points))
            
            fig, axs = plt.subplots(1, 2, figsize=(12, 8))
            
            # Fit a Burr Type XII distribution to the data
            fit_params = stats.burr12.fit(times)

            # Create a Burr distribution object with the fitted parameters
            fitted_dist = stats.burr12(*fit_params)

            print(f"Burr12 params: {fit_params} | Mean {fitted_dist.mean()} | Median {fitted_dist.median()} | WR CDF: {fitted_dist.cdf(data[0]['time'])} | Last place: {fitted_dist.cdf(data[-1]['time'])}")
            # Create a histogram of the data
            axs[0].hist(times, bins=100, density=True, alpha=0.6, label='Times Histogram')

            # Create a curve based on the fitted distribution
            x = np.linspace(times.min(), times.max(), 100)
            axs[0].plot(x, fitted_dist.pdf(x), 'r', lw=1, label='Fitted BurrXII PDF')

            axs[0].set_xlabel('Time')
            axs[0].set_ylabel('Density')
            axs[0].set_title('Fitted BurrXII PDF')
            axs[0].legend()
            
            axs[1].plot(x, fitted_dist.cdf(x), 'r', lw=1, label='Fitted BurrXII CDF')
            axs[1].set_title('Fitted BurrXII CDF')
            
            plt.tight_layout()
            
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            plt.savefig(f"{output_path}/{filename.removesuffix('.json')}.png", dpi = 500)
            
            