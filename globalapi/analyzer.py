# KZ map points calculator for current system
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from scipy.stats._continuous_distns import _distn_names
import warnings

# Create models from data
def best_fit_distribution(data, bins=200, top=10):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Best holders
    best_distributions = []

    # Estimate distribution parameters from data
    for ii, distribution in enumerate([d for d in _distn_names if not d in ['studentized_range', 'burr12', 'foldcauchy', 'gennorm', 'cauchy', 't', 'johnsonsu',
                                                                            'powernorm', 'mielke', 'dweibull', 'rel_breitwigner', 'tukeylambda', 'skewcauchy', 'laplace_asymmetric',
                                                                            'genhyperbolic', 'erlang', 'fatiguelife', 'gausshyper', 'loglaplace', 'geninvgauss']]):


        dist = getattr(stats, distribution)

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                
                # fit dist to data
                params = dist.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]
                
                # Calculate fitted PDF and error with fit in distribution
                pdf = dist.pdf(x, loc=loc, scale=scale, *arg)
                mse = np.sum(np.power(y - pdf, 2.0))/len(y)

                # identify if this distribution is better
                best_distributions.append((distribution, params, mse, dist))
        except Exception:
            pass
    return sorted(best_distributions, key=lambda x:x[2])[0:top]

def print_top_common_occurrences(list, n=5):
    occurrences = {}
    for e in list:
        if e in occurrences:
            occurrences[e] += 1
        else:
            occurrences[e] = 1

    common_occurrences = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)[:n]

    print(f"Top {n} most common occurrences:")
    for value, count in common_occurrences:
        print(f"{value}: {count} occurrences")

path = 'data'
output_path = 'graphs'
all_dists = []
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
            
            # Remove rank-based rewards
            data[0]['points'] -= 200
            for i in range(1,len(data)):
                rankfactor = 198 - i * 2
                if rankfactor < 0: rankfactor = 0
                data[i]['points'] -= rankfactor
                
            points = np.array([record['points'] for record in data])
            times = np.array([(record['time']) for record in data])
            print("Mean / Median:", times.mean(), np.median(times))
            print("Top 5 times:", data[0]['time'], data[1]['time'], data[2]['time'], data[3]['time'] , data[4]['time'])
            print("Top 1% / 10% / 25% / 50% / 75%:", np.percentile(times, 1), np.percentile(times, 10), np.percentile(times, 25), np.percentile(times, 50), np.percentile(times, 75))
            print("Bottom 5 times:", data[-1]['time'], data[-2]['time'], data[-3]['time'], data[-4]['time'] , data[-5]['time'])
            fig, axs = plt.subplots(3, 2, figsize=(12, 8))
            
            # Fit a Burr Type XII distribution to the data
            burr12_params = stats.burr12.fit(times)

            # Create a Burr distribution object with the fitted parameters
            burr12_dist = stats.burr12(*burr12_params)

            print(f"Burr12 params: {burr12_params} | Mean {burr12_dist.mean()} | Median {burr12_dist.median()} | WR CDF: {burr12_dist.cdf(data[0]['time'])} | Last place: {burr12_dist.cdf(data[-1]['time'])}")
            
            norminvgauss_params = stats.norminvgauss.fit(times)
            norminvgauss_dist = stats.norminvgauss(*norminvgauss_params)

            print(f"Norminvgauss params: {norminvgauss_params} | Mean {norminvgauss_dist.mean()} | Median {norminvgauss_dist.median()} | WR CDF: {norminvgauss_dist.cdf(data[0]['time'])} | Last place: {norminvgauss_dist.cdf(data[-1]['time'])}")
            print(f"Estimating best distributions...")
            distributions = best_fit_distribution(times)
            for dist in distributions:
                print(dist[0], dist[2])
                all_dists.append(dist[0])
            # Create a histogram of the data
            axs[0,0].hist(times, bins=200, density=True, alpha=0.6, label='Times Histogram', range = [0,np.median(times)*4])

            # Create a curve based on the fitted distribution
            x = np.linspace(0, times.max(), 200)
            
            axs[0,0].plot(x, burr12_dist.pdf(x), 'r', lw=1, label='Fitted BurrXII PDF')
            axs[0,0].plot(x, norminvgauss_dist.pdf(x), 'y', lw=1, label='Fitted norminvgauss PDF')
            


            axs[0,0].set_xlabel('Time')
            axs[0,0].set_ylabel('Density')
            axs[0,0].set_title('Times')
            axs[0,0].legend()
            
            axs[0,1].hist(times, bins=300, density=True, cumulative=True, alpha=0.6, label='Times Histogram', range = [0,np.mean(times)*4])
            
            axs[0,1].set_xlabel('Time')
            # for dist in distributions:
            #     axs[0,1].plot(x, dist[3](*dist[1]).cdf(x), lw=1, label=dist[0])
            axs[0,1].plot(x, burr12_dist.cdf(x), 'r', lw=1, label='Fitted BurrXII CDF')
            axs[0,1].plot(x, norminvgauss_dist.cdf(x), 'y', lw=1, label='Fitted norminvgauss CDF')
            axs[0,1].set_title('Times CD')
            bins_count = 80
            axs[1,0].hist(points, bins=bins_count, density=True, alpha=0.6, label='Points Histogram', color='red', range=[0, 800])
            axs[1,0].set_title('Burr12 Points PD')
            axs[1,1].hist(points, bins=bins_count, density=True, cumulative=True, alpha=0.6, label='Points Histogram', color='red', range=[0, 800])
            axs[1,1].set_title('Burr12 Points CD')

            new_points = 800 * (norminvgauss_dist.sf(times)) / norminvgauss_dist.sf(times[0])
            axs[2,0].hist(new_points, bins=bins_count, density=True, alpha=0.6, label='Experimental Points Histogram', color='y', range=[0, 800])
            axs[2,0].set_title('Norminvgauss Points PD')
            axs[2,1].hist(new_points, bins=bins_count, density=True, cumulative=True, alpha=0.6, label='Experimental Points Histogram', color='y', range=[0, 800])
            axs[2,1].set_title('Norminvgauss Points CD')
            
            axs[2,1].sharey(axs[1,1])
            axs[2,0].sharey(axs[1,0])
            
            for i in range(1,3):
                for j in range(0,2):
                    axs[i,j].set_xlabel('Points')
                axs[i,0].set_ylabel('Density')
                axs[i,1].set_ylabel('Percentage')
                if i > 0:
                    axs[i,0].axhline(0.1/bins_count, color = 'black', linestyle = 'dashed', lw = 1) # bin width is 10
            plt.tight_layout()
            plt.suptitle(f"{map_name}({map_info[1]})")
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            plt.savefig(f"{output_path}/{filename.removesuffix('.json')}.png", dpi = 500)

print_top_common_occurrences(all_dists, 120)