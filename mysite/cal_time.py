import numpy as np
import random
from mysite.rcexp.models import Network_Structure, Exp_Info
import json

def travel_time_function(link_flow, free_flow_time,link_capacity):
	t=free_flow_time*(1+0.15*(link_flow/link_capacity)**4)
	return t

# od_demand=5;
# link_path_matrix=np.array([[1, 0, 0], [0, 1, 1], [1, 0, 1], [0, 1, 0], [0, 0, 1]])
# free_flow_time=np.array([2, 1, 1, 2, 1])
# link_capacity=np.array([3, 7, 7, 3, 4])

def cal_path_time(path_flow, exp_id):
	p = Exp_Info.objects.get(exp_id=exp_id)
	link_path_matrix = json.loads(p.link_path_matrix)
	link_path_matrix = np.array(link_path_matrix)
	link_num = p.link_num
	path_num = p.path_num
	free_flow_time = json.loads(p.free_flow_time)
	free_flow_time = np.array(free_flow_time)
	link_capacity = json.loads(p.link_capacity)
	link_capacity = np.array(link_capacity)
	# od_demand = p.od_demand
	link_flow=np.dot(link_path_matrix, path_flow)
	link_time=travel_time_function(link_flow,free_flow_time,link_capacity)
	path_time=(np.dot(link_path_matrix.transpose(), link_time)).tolist()
	# print('link_path_matrix\n', link_path_matrix)
	# print('path_flow', path_flow)
	# print('link_flow', link_flow)
	# print('link_time', link_time)
	# print('path_time', path_time)
	# print('link_capacity', link_capacity)
	return path_time
