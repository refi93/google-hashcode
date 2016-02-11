import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

np.set_printoptions(threshold=np.nan)

def getBitmap(rows, cols, warehouses):
	bitmap = np.zeros(shape=(rows,cols))
	for warehouse in warehouses:
		bitmap[warehouse[0], warehouse[1]] = 1

	return bitmap

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

print (sum_order_count * 1.0 / order_count)
print max_order_count

plt.imsave('warehouses.png', getBitmap(rows, cols, warehouses), cmap=cm.gray)
plt.imsave('orders.png', getBitmap(rows, cols, orders_delivery_addresses), cmap=cm.gray)
