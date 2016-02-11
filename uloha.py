import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

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
	for i in len(warehouses):
		w = warehouse[i]
		cur_dist = getDist(r, c, w[0], w[1])
		if (cur_dist < best_warehouse_dist):
			best_warehouse_dist = cur_dist
			best_warehouse_id = i

	return best_warehouse_id

def reserveItemAtWarehouse(item_id, warehouse_id):
	if warehouses_items[warehouse_id][item_id] == 0:
		print str(item_id) + " is not present at warehouse " + warehouse_id
		exit(1)
	warehouses_items[warehouse_id][item_id]--

def getOrderItemList():
	item_queues = []
	indexes = np.random.permutation(order_count)
	for i in indexes:
		address = orders_delivery_addresses[i]
		for item in order_items[i]:
			item_queues.append((item, address))
	return item_queues


def initDroneQueue():
	dron_queue = defaultdict(set)
	start = warehouses[0]
	for i in range(drone_count):
		dron_queue[0].add((i, start))	
	return dron_queue


s = sys.stdin

l = s.readline().split()
rows = int(l[0])
cols = int(l[1])
drone_count = int(l[2])
turns = int(l[3])
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

dron_queue = initDroneQueue()
order_item_list = getOrderItemList()

# print (sum_order_count * 1.0 / order_count)
# print max_order_count

# plt.imsave('warehouses.png', getBitmap(rows, cols, warehouses), cmap=cm.gray)
# plt.imsave('orders.png', getBitmap(rows, cols, orders_delivery_addresses), cmap=cm.gray)
