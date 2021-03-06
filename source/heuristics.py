import random
import math

# utility functions
def distance(lhs, rhs):
	s = 0
	for i in range(len(lhs)):
		s += (lhs[i] - rhs[i]) ** 2
	return math.sqrt(s)
	
def location(entity):
	return (entity['x'], entity['y'], entity['z'])
	
def dot(lhs, rhs):
	s = 0
	for i in range(len(lhs)):
		s += lhs[i] * rhs[i]
	return s
	
def diff(lhs, rhs):
	return tuple([lhs[i] - rhs[i] for i in range(len(lhs))])
	
def magnitude(v):
	s = 0
	for i in range(len(v)):
		s += v[i] * v[i]
	return math.sqrt(s)
	
def normalize(v):
	m = magnitude(v)
	return tuple([i / m for i in v])
	
def get_player_location(el):
	for e in el:
		if e[u'name'] == u'PacManBot':
			return location(e)
			
	return None
	
def get_closest_entity(el, entity_name):
	playerLoc = get_player_location(el)

	closest_distance = 100000
	closest_entity = None
	
	for e in el:
		d = distance(location(e), playerLoc)
		if e[u'name'] != entity_name or d > closest_distance:
			continue
		
		closest_distance = d
		closest_entity = e
	
	if closest_entity == None:
		return None, (None, None, None)
			
	return closest_entity, diff(location(closest_entity), playerLoc)
	
def closest_cardinals(dir, obs):
	dir = normalize(dir)
	actions_list = []

	if obs.grid[1] == u'glowstone':
		actions_list.append(('movenorth 1', dot(dir, (0, 0, -1))))
	if obs.grid[3] == u'glowstone':
		actions_list.append(('movewest 1', dot(dir,(-1, 0, 0))))
	if obs.grid[5] == u'glowstone':
		actions_list.append(('moveeast 1', dot(dir, (1, 0, 0))))
	if obs.grid[7] == u'glowstone':
		actions_list.append(('movesouth 1', dot(dir, (0, 0, 1))))
		
	actions_list.sort(key = lambda d: d[1])
	return [a[0] for a in actions_list]
	
def opposite_direction(dir):
	if dir == 'movesouth 1':
		return 'movenorth 1'
	elif dir == 'moveeast 1':
		return 'movewest 1'
	elif dir == 'movenorth 1':
		return 'movesouth 1'
	return 'moveeast 1'

#heuristic functions
def random_direction(obs):
	actions_list = []
	if(obs.grid[1] == u'glowstone'):
		actions_list.append('movenorth 1')
	if(obs.grid[3] == u'glowstone'):
		actions_list.append('movewest 1')
	if(obs.grid[5] == u'glowstone'):
		actions_list.append('moveeast 1')
	if(obs.grid[7] == u'glowstone'):
		actions_list.append('movesouth 1')

	if len(actions_list) == 0:
		return "quit"

	r = random.random()
	a = random.randint(0, len(actions_list) - 1)
	return actions_list[a]

def away_from_enemy(obs):
	closest_entity, dir = get_closest_entity(obs.entity_locations, u'Zombie')
		
	if closest_entity == None:
		return random_direction(obs)
		
	return closest_cardinals(dir, obs)[0]
	
def towards_item(obs):
	closest_entity, dir = get_closest_entity(obs.entity_locations, u'diamond')
	
	if closest_entity == None:
		return random_direction(obs)
		
	return closest_cardinals(dir, obs)[-1]
    
def away_from_edges(obs):
	min_dist = min(obs.edge_distances)

	actions_list = []
	if obs.edge_distances[0] == min_dist and obs.grid[7] == u'glowstone':
		actions_list.append('movesouth 1')
	if obs.edge_distances[1] == min_dist and obs.grid[3] == u'glowstone':
		actions_list.append('movewest 1')
	if obs.edge_distances[2] == min_dist and obs.grid[1] == u'glowstone':
		actions_list.append('movenorth 1')
	if obs.edge_distances[3] == min_dist and obs.grid[5] == u'glowstone':
		actions_list.append('moveeast 1')
	
	if len(actions_list) == 0:
		return random_direction(obs)
	
	a = random.randint(0, len(actions_list) - 1)
	return actions_list[a]
	
def towards_edges(obs):
	return opposite_direction(away_from_edges(obs))