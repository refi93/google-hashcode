import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
# import Queue
from Queue import Queue
from collections import defaultdict


np.set_printoptions(threshold=np.nan)

def getBitmap(rows, cols, warehouses):
	bitmap = np.zeros(shape=(rows,cols))
	for warehouse in warehouses:
		bitmap[warehouse[0], warehouse[1]] = 1

	return bitmap

def getDist(r1, c1, r2, c2):
	return math.ceil(math.sqrt((r1 - r2)**2 + (c1 - c2)**2))

def getNearestWarehouseId(r, c, item_id):
	best_warehouse_dist = 100000000
	best_warehouse_id = 0 
	for i in range(len(warehouses)):
		w = warehouses[i]
		if (warehouses_items[i][item_id] > 0):
			cur_dist = getDist(r, c, w[0], w[1])
			if (cur_dist < best_warehouse_dist):
				best_warehouse_dist = cur_dist
				best_warehouse_id = i

	return best_warehouse_id

def reserveItemAtWarehouse(item_id, warehouse_id):
	if warehouses_items[warehouse_id][item_id] == 0:
		print str(item_id) + " is not present at warehouse " + str(warehouse_id)
		exit(1)
	warehouses_items[warehouse_id][item_id] -= 1


def orderEasiness(order_id):
	easiness = 0
	address = orders_delivery_addresses[order_id]
	items = orders_items[order_id]
	for item in items:
		nw_id = getNearestWarehouseId(address[0], address[1], item)
		nw_address = warehouses[nw_id] 
		easiness += 2 * getDist(address[0], address[1], nw_address[0], nw_address[1])

	return easiness

def getOrderItemQueue():
	item_queue = Queue()
	indexes = np.random.permutation(order_count)
	indexes = sorted(list(range(order_count)), key=lambda x: orderEasiness(x))
	for i in indexes:
		address = orders_delivery_addresses[i]
		for item in orders_items[i]:
			item_queue.put((item, address, i))
	return item_queue


# def getOrderItemQueue():
# 	item_queue = Queue()
# 	indexes = np.random.permutation(order_count)
# 	for i in indexes:
# 		address = orders_delivery_addresses[i]
# 		for item in orders_items[i]:
# 			item_queue.put((item, address, i))
# 	return item_queue

def getEstimateTimeOfTask(drone_r, drone_c, warehouse_id, addr_r, addr_c):
	warehouse_r = warehouses[warehouse_id][0]
	warehouse_c = warehouses[warehouse_id][1]
	return getDist(drone_r, drone_c, warehouse_r, warehouse_c) + getDist(warehouse_r, warehouse_c, addr_r, addr_c) + 2

def initDroneQueue():
	dron_queue = defaultdict(set)
	start = warehouses[0]
	for i in range(drone_count):
		dron_queue[0].add((i, tuple(start)))	
	return dron_queue

def performTurn():
	free_drones = drone_queue[current_turn]
	while free_drones:
		if (order_item_queue.empty()):
			return False
		item_to_process = order_item_queue.get()
		drone = free_drones.pop()
		item_id = item_to_process[0]
		order_id = item_to_process[2]
		drone_id = drone[0]
		delivery_address = item_to_process[1]

		# finding the nearer of two warehouses
		nearest_warehouse_id = 0
		estimate_task_time = 10000000
		nearest_warehouse_id_to_drone = getNearestWarehouseId(drone[1][0], drone[1][1], item_id)
		estimate_task_time_drone = getEstimateTimeOfTask(drone[1][0], drone[1][1], nearest_warehouse_id_to_drone, delivery_address[0], delivery_address[1])

		nearest_warehouse_id_to_delivery_address = getNearestWarehouseId(delivery_address[0], delivery_address[1], item_id)
		estimate_task_time_delivery_address = getEstimateTimeOfTask(drone[1][0], drone[1][1], nearest_warehouse_id_to_delivery_address, delivery_address[0], delivery_address[1])

		if (estimate_task_time_delivery_address > estimate_task_time_drone):
			nearest_warehouse_id = nearest_warehouse_id_to_drone
			estimate_task_time = estimate_task_time_drone
		else:
			nearest_warehouse_id = nearest_warehouse_id_to_delivery_address
			estimate_task_time = estimate_task_time_delivery_address

		if (estimate_task_time > turns - current_turn):
			return False

		command_list.append("{} L {} {} {}".format(drone_id, nearest_warehouse_id, item_id, 1) )
		command_list.append("{} D {} {} {}".format(drone_id, order_id, item_id, 1) )
		
		reserveItemAtWarehouse(item_id, nearest_warehouse_id)
		drone_queue[current_turn + estimate_task_time].add((drone[0], tuple(delivery_address)))
	return True


s = sys.stdin

l = s.readline().split()
rows = int(l[0])
cols = int(l[1])
drone_count = int(l[2])
turns = int(l[3])
current_turn = 0
max_payload = int(l[4])

product_count = int(s.readline())
products = [ int(p) for p in s.readline().split() ]

warehouse_count = int(s.readline())
warehouses = []
warehouses_items = []

for i in range(0, warehouse_count):
	warehouse_coords = [ int(wc) for wc in s.readline().split() ]
	warehouse_items = [ int(wi) for wi in s.readline().split() ]

	warehouses.append(warehouse_coords)
	warehouses_items.append(warehouse_items)


order_count = int(s.readline())
orders_delivery_addresses = []
orders_items = []
max_order_count = 0
sum_order_count = 0
for i in range(0, order_count):
	order_delivery_address = [ int(addr) for addr in s.readline().split() ]
	order_items_count = int(s.readline())
	order_items = [ int(item) for item in s.readline().split() ]
	max_order_count = max(max_order_count, len(order_items))
	sum_order_count += len(order_items)
	orders_delivery_addresses.append(order_delivery_address)
	orders_items.append(order_items)

drone_queue = initDroneQueue()
order_item_queue = getOrderItemQueue()
command_list = []

while performTurn():
	current_turn += 1

print len(command_list)
for command in command_list:
	print command
# print (sum_order_count * 1.0 / order_count)
# print max_order_count

# plt.imsave('warehouses.png', getBitmap(rows, cols, warehouses), cmap=cm.gray)
# plt.imsave('orders.png', getBitmap(rows, cols, orders_delivery_addresses), cmap=cm.gray)
