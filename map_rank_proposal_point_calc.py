
import numpy as np

def get_distribution_points_portion_under_50(time, wr_time, tier):
    return ((1+np.exp((2.1 - 0.25 * tier) * -0.5))/(1+np.exp((2.1 - 0.25 * tier) * (time/wr_time-1.5))))


def get_rank_points_portion(rank, total):
    if rank < 0:
        return 0
    # 50% relative total amount of completions, 50% based on top 100/20/5
    points = 0.5 * (1 - rank / total)

    if rank < 100:
        points += (100 - rank) * 0.002 # max of 0.2
    if rank < 20:
        points += (20 - rank) * 0.01 # max of 0.2
    match rank:
        case 4:
            points += 0.01
        case 3:
            points += 0.03
        case 2:
            points += 0.045
        case 1:
            points += 0.06
        case 0:
            points += 0.1
    return points

def get_min_tier_points(tier, pro = False):
    points = 0
    match tier:
        case 2:
            points = 500
        case 3:
            points = 2000
        case 4:
            points = 3500
        case 5:
            points = 5000
        case 6:
            points = 6500
        case 7:
            points = 8000
        case 8:
            points = 9500
    if pro:
        points += (10000 - points) * 0.1
    return points

def get_points(dist, time, wr_time, tier, rank, total, pro, dist_wr_sf):
    min_points = get_min_tier_points(tier, pro)
    remaining_points = 10000 - min_points

    dist_points = remaining_points * 0.75
    rank_points = remaining_points * get_rank_points_portion(rank, total) * 0.25

    if total < 50:
        dist_points *= get_distribution_points_portion_under_50(time, wr_time, tier)
    else:
        # 1-cdf is faster but less accurate
        dist_points *= (1 - dist.cdf(time)) / dist_wr_sf

    return int(min_points + dist_points + rank_points)
