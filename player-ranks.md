(wip)

# Goal
- Make this an actual indicator of skill to some extent

# Description of current systems
<details>
  <summary><b><font size = "+2">Current system, SurfTimer, KSF</font></b></summary>

Sum of points


### Note:
  - More completions is king, unless the drop in points is extremely steep, then more WRs is king.
</details>

<details>
  <summary><b><font size = "+2">GameChaos's 2020 formula</font></b></summary>


multiplier = finishes^0.2 / mapcount^0.2
skill = averagePoints * multiplier

### Note:
  - Completion is king, but not as much as the sum of points method.
  - Completion on low tier has the same impact as high tier (probably bad?)
  - Can get away with high enough multiplier and cheese for skill: Doing every map but the maps on the two hardest tiers makes the multiplier 0.98, at this point doing harder tier maps is a bad strategy if a high points reward is unlikely.
</details>

<details>
  <summary><b><font size = "+2">GOKZCN (X1's) formula</font></b></summary>

```
p = ((
　　(count_p1000_nub/count_map)^(1/3.5)*1.1 + (count_p1000_pro/count_map)^(1/2.4)*6 + (count_p900/count_map)^(1/2)*.14 + (count_p800/count_map)^(1/2)*.04

　　+ point_avg/1000*.07 + point_avg_t3/1000*.01 + point_avg_t4/1000*.02 + point_avg_t5/1000*.1 + point_avg_t6/1000*.12 + point_avg_t7/1000*.17

　　+ count/count_map*.01 + (count_t5/count_map_t5)^(1/1.5)*.05 + (count_t6/count_map_t6)^(1/1.5)*.15 + (count_t7/count_map_t7)^(1/1.5)*.24

　　+ point_sum/1000/count_map*.01 + count_t567_p900/count_map_t567*.06 + count_t567_p800/count_map_t567*.03 + count_t567_pro/count_map_t567*.06

)/8.38)^(1/8)/0.91*10
```
### Note:
- Depends quite a bit on the currently flawed map points system.
- WR matters way too much, so much that it needs a 8th root at the end to compensate for the extreme gap in #1 and #2 points.
- Allegedly isn't too useful for lower ranked players.
- Has some point-based and completion-based component, albeit nowhere as significant as getting a WR or having a 800/900+ points map (and difficulty of getting 800/900 points is wildly inconsistent)
</details>

<details>
  <summary><b><font size = "+2">Jak's system</font></b></summary>

https://forum.gokz.org/d/3781-cs2kz-what-would-you-change/61
2 simutaneous systems, one using average, another using sum of points

### Note:
- Having 2 simutaneous systems is having one too many, just confusing for players
- Average is stupidly cheeseable by just playing one map.
- Sum of points is hardly an indicator of skill (if at all, see current system). Doing 11 tier 4 maps gives the same points as a WR on a tier 4 map.
</details>

<details>
  <summary><b><font size = "+2">Szwagi's system</font></b></summary>

  https://forum.gokz.org/d/3781-cs2kz-what-would-you-change/74


```
I'd like to see weighting added to the points.
To calculate overall points, sort the player's points highest to lowest, then apply this formula:

overall_points += run_points * 0.975^(n-1)
This would cause ranks and point leaderboards to be more competitive. Right now you can get more points
by simply playing more maps (and there's always more maps for you unless you're Blacky), even if you're only getting 500 points a map.

This is pretty much point average without ever being able to lower it by playing a map you're not that great on.
```


### Note:

- Straight up better than current system which is literally just sum of points.

- 40000 max points

- Top 20 maps account for 40% of total points, 50 for 72%, 100 for 92% of total points and 200 for 99.7% of total points
  - With 1000 KZ maps, there are little reasons to complete the other 800 maps if high points are not guaranteed, similar to GC 2020's idea
  - Players can have a high rank by being really good at easy maps even if they are completely incapable of completing any hard map
</details>
