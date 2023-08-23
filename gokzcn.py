# Formula majorly based on X1's gokz.cn formula

# Sample players
PLAYERS = [
	(76561198325578948, "smieszneznaczki"),
	(76561198118681904, "zer0.k"),
	(76561198349042363, "sampge"),
	(76561198317412990, "AyayaBoy"),
	(76561198091592005, "Blacky"),
	(76561198857828380, "Szwagi"),
	(76561198399413724, "今生-Lzd"),
	(76561198033461776, "gwooky"),
	(76561198194803245, "neon"),
	(76561198193745669, "Mugen"),
	(76561198049744493, "clear"),
	(76561198231238712, "jucci"),
	(76561197983508357, "Kurbashi"),
	(76561198008185887, "LEWLY"),
	(76561198072210646, "Fafnir"),
	(76561198149087452, "Kuu"),
	(76561197963395006, "FrozeEnd"),
	(76561198023573197, "Ebun"),
	(76561198300753898, "Nuke"),
	(76561198097865637, "LEO"),
	(76561197998046384, "FFM"),
	(76561197981712950, "Jakke"),
	(76561198046784327, "Sachburger"),
	(76561197983014207, "Zach47"),
	(76561198297415967, "Flonny"),
	(76561198205898656, "GiimPy"),
	(76561198014491259, "nykaN"),
	(76561198204867971, "Kuupo"),
	(76561198078014747, "iBUYFL0WER Burgit"),
	(76561198260657129, "ReDMooN"),
	(76561198004411671, "Linus"),
	(76561198262372665, "iEatCrayons"),
	(76561198100183392, "Ruben"),
	(76561198057269402, "Orbit")
]
MAPS = []
MAP_TIERS = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
import requests
import json

class Map:
	def __init__(self, id, name, difficulty):
		self.id = id
		self.name = name
		self.difficulty = difficulty

class Record:
	def __init__(self, map: Map, pro: bool, points: int):
		self.map = map
		self.pro = pro
		self.points = points

def init_maps():
	global MAPS, MAP_TIERS
	url = "https://kztimerglobal.com/api/v2/maps?limit=9999"
	
	response = requests.get(url)
	
	if response.status_code == 200:
		json_data = response.json()  # Parse JSON response into a dictionary
		for map in json_data:
			if not map['validated']: continue
			MAPS.append(Map(map['id'], map['name'], map['difficulty']))
			MAP_TIERS[str(map['difficulty'])] += 1
	else:
		print("Error:", response.status_code)

def get_map(id) -> Map:
	global MAPS
	map: Map
	for map in MAPS:
		if map.id == id:
			return map
	return None # type: ignore
	
def add_record_to_record_list(record_list: list, record: Record):				
	rec: Record
	found = False
	for rec in record_list:
		if (rec.map.id == record.map.id or rec.map.name == record.map.name) and record.points > rec.points:
			rec.points = record.points
			break
	if not found:
		record_list.append(record)
		
def get_player_records(steamid64):
	# KZT only for now
	url = f"https://kztimerglobal.com/api/v2/records/top?steamid64={steamid64}&tickrate=128&stage=0&modes_list_string=kz_timer&limit=2000"
	
	response = requests.get(url)

	if response.status_code == 200:
		json_data = response.json()
		pro_records = []
		nub_records = []
			
		for record in json_data:
			# Invalid map check
			if get_map(record['map_id']) is None: continue 
			
			# Add run to list of runs
			# When a tp run and a pro run both exist, the nub run is the one with more points
			pro = record['teleports'] == 0
			rec = Record(get_map(record['map_id']), pro, record['points'])

			add_record_to_record_list(nub_records, rec)
			if pro:
				add_record_to_record_list(pro_records, rec)

		return nub_records,pro_records
	else:
		print("Error:", response.status_code)
		return None, None

def get_total_points(record_list: list, difficulty: int) -> int:
	if difficulty == 0:
		return sum(record.points for record in record_list)
	else:
		total = 0
		record: Record
		for record in record_list:
			if record.map.difficulty == difficulty:
				total += record.points
	return total

def get_num_record_difficulty(record_list: list, difficulty: int) -> int:
	if difficulty == 0:
		return len(record_list)
	else:
		num_maps = 0
		record: Record
		for record in record_list:
			if record.map.difficulty == difficulty:
				num_maps += 1
		return num_maps

def get_average_points(record_list: list, difficulty: int) -> float:
	num_maps = get_num_record_difficulty(record_list, difficulty)

	if num_maps == 0: 
		return -1.0
	return get_total_points(record_list, difficulty) / num_maps

def get_num_records_at_min_point(record_list: list, threshold: int) -> int:
	record: Record
	count = 0
	for record in record_list:
		if record.points >= threshold:
			count += 1
	return count

def get_num_records_at_difficulty_and_min_point(record_list: list, difficulty: int, threshold: int) -> int:
	record: Record
	count = 0
	for record in record_list:
		if record.points >= threshold and record.map.difficulty == difficulty:
			count += 1
	return count

def get_rank(nub_records, pro_records):
	count_t567_p800 = get_num_records_at_difficulty_and_min_point(nub_records, 5, 800) + \
					get_num_records_at_difficulty_and_min_point(nub_records, 6, 800)   + \
					get_num_records_at_difficulty_and_min_point(nub_records, 7, 800)

	count_t567_p900 = get_num_records_at_difficulty_and_min_point(nub_records, 5, 900) + \
					get_num_records_at_difficulty_and_min_point(nub_records, 6, 900)   + \
					get_num_records_at_difficulty_and_min_point(nub_records, 7, 900)

	count_t567_pro = get_num_record_difficulty(pro_records, 5) + get_num_record_difficulty(pro_records, 6) + get_num_record_difficulty(pro_records, 7)
	count_map_t567 = MAP_TIERS["5"] + MAP_TIERS["6"] + MAP_TIERS["7"]

	rank_factor =	(get_num_records_at_min_point(pro_records, 1000) / len(MAPS)) **(1/2.4)	* 6		+ \
					(get_num_records_at_min_point(nub_records, 1000) / len(MAPS)) **(1/3.5)	* 1.1	+ \
					(get_num_records_at_min_point(nub_records, 900) / len(MAPS))  **(1/2)	* 0.14	+ \
					(get_num_records_at_min_point(nub_records, 800) / len(MAPS))  **(1/2)	* 0.04

	pt_factor =		(get_average_points(nub_records, 0) / 1000)								* 0.07	+ \
					(get_average_points(nub_records, 3) / 1000)								* 0.01	+ \
					(get_average_points(nub_records, 4) / 1000)								* 0.02	+ \
					(get_average_points(nub_records, 5) / 1000)								* 0.1	+ \
					(get_average_points(nub_records, 6) / 1000)								* 0.12	+ \
					(get_average_points(nub_records, 7) / 1000)								* 0.17	+ \
					(get_total_points(nub_records, 0)   / 1000 / len(MAPS))					* 0.01

	compl_factor =  (get_num_record_difficulty(nub_records, 0) / len(MAPS))					* 0.01	+ \
					(get_num_record_difficulty(nub_records, 5) / MAP_TIERS["5"])			* 0.05	+ \
					(get_num_record_difficulty(nub_records, 6) / MAP_TIERS["6"])			* 0.15	+ \
					(get_num_record_difficulty(nub_records, 7) / MAP_TIERS["7"])			* 0.24	+ \
					(count_t567_p900 / count_map_t567)										* 0.06	+ \
					(count_t567_p800 / count_map_t567)										* 0.03	+ \
					(count_t567_pro / count_map_t567)										* 0.06

	return ((rank_factor + pt_factor + compl_factor) / 8.38) ** (1/8) / 0.91 * 10

init_maps()
ranks = []
for player in PLAYERS:
	nub_records, pro_records = get_player_records(player[0])
	rank = get_rank(nub_records, pro_records)
	ranks.append((player[1], rank))
	print(f"{player[1]} - {rank}")

sorted_ranks = sorted(ranks, key = lambda x: x[1], reverse=True)
print("Player - Ranks:")
for player in sorted_ranks:
	print(f"{player[0]} - {player[1]}")

