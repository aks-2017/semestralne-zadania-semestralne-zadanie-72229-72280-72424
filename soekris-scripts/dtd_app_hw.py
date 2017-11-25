import requests
import json
import time
import os

upperThreshold = 0.9
lowerThreshold = 0.7
primaryRoute = 0
backupRoute = 1
max_speed = 10485760/8
state = primaryRoute
B_to_MB = float(1024**2)

controller = 'http://127.0.0.1:8080'
h1_mac = '00:0c:29:95:dc:64'
h2_mac = '00:0a:cd:29:42:c1'
h3_mac = '00:1f:16:ac:df:9d'
h4_mac = '00:1f:16:ac:df:9d'

class Router(object):
	def __init__(self,j):
		self.__dict__ = j.json()[0]

def getPortStatsInfo():
	r = requests.get(controller + '/stats/port/617684205/2')
	return r.json()['617684205'][0]['tx_bytes']

def getPortStatsInfo1():
        r = requests.get(controller + '/stats/port/617684205/3')
        return r.json()['617684205'][0]['tx_bytes']	

def add_flow(dpid, priority, src_mac, in_port, output_port):
	url = controller + '/stats/flowentry/add'
	
	data = {}
	data['dpid'] = dpid
	data['priority'] = priority
	data['match'] = {'eth_src': src_mac, 'in_port': in_port}
	data['actions'] = [{'type': 'OUTPUT', 'port': output_port}]
	
	r = requests.post(url, json.dumps(data))
	
	if r.status_code is 200:
		print('SW'+ str(dpid) + '. Added flow.' )
	else:
		print('SW'+ str(dpid) + '. None added flow.' )

def add_def_flow(dpid, in_port):
	url = controller + '/stats/flowentry/add'
	
	data = {}
	data['dpid'] = dpid
	data['priority'] = 1
	data['match'] = {'in_port': in_port}
	data['actions'] = []
	
	r = requests.post(url, json.dumps(data))
	
	if r.status_code is 200:
		print('SW'+ str(dpid) + '. Added flow.' )
	else:
		print('SW'+ str(dpid) + '. None added flow.' )

def modify_flow(dpid, priority, src_mac, in_port, output_port):
        url = controller + '/stats/flowentry/modify'

        data = {}
        data['dpid'] = dpid
        data['priority'] = priority
        data['match'] = {'eth_src': src_mac, 'in_port': in_port}
        data['actions'] = [{'type': 'OUTPUT', 'port': output_port}]

        r = requests.post(url, json.dumps(data))

        if r.status_code is 200:
                print('SW'+ str(dpid) + '. Modified flow.' )
        else:
                print('SW'+ str(dpid) + '. None modified flow.' )

def switch_route(state):
	if state is backupRoute:
		modify_flow(617684205, 65535, h1_mac, 1, 3)
		modify_flow(617684205, 65535, h3_mac, 3, 1)
	
	if state is primaryRoute:
		modify_flow(617684205, 65535, h1_mac, 1, 2)
		modify_flow(617684205, 65535, h3_mac, 2, 1)


#config switch 1
add_flow(617684205, 65535, h1_mac, 1, 2)
add_flow(617684205, 65535, h3_mac, 2, 1)
add_flow(617684205, 65535, h2_mac, 1, 2)
add_def_flow(617684205, 1)
add_def_flow(617684205, 2)
add_def_flow(617684205, 3)
#add_flow(617684205, 65535, h4_mac, 2, 1)
#add_flow(1, 65535, h3_mac, 3, 1)

#config switch 3
'''add_flow(3, 65535, h3_mac, 1, 4)
add_flow(3, 65535, h1_mac, 4, 1)
add_flow(3, 65535, h4_mac, 2, 4)
add_flow(3, 65535, h2_mac, 4, 2)
add_flow(3, 65535, h1_mac, 3, 1)

#config switch 2
add_flow(2, 65535, h1_mac, 1, 2)
add_flow(2, 65535, h3_mac, 2, 1)
'''

totalTxBytes = getPortStatsInfo() 
totalTxBytesBckp = getPortStatsInfo1()

while True:
	oldTxBytes = totalTxBytes
	totalTxBytes = getPortStatsInfo()
	currentTxBytes = totalTxBytes - oldTxBytes

	oldTxBytesBckp = totalTxBytesBckp
	totalTxBytesBckp = getPortStatsInfo1()
	currentTxBytesBckp = totalTxBytesBckp - oldTxBytesBckp
	
	'''if totalTxBytes != oldTxBytes:
		print(currentTxBytes)
		print(max_speed * upperThreshold)
		if (currentTxBytes) > (max_speed * upperThreshold) and state is primaryRoute:
			state = backupRoute
			switch_route(state)
		if (currentTxBytes) < (max_speed * lowerThreshold) and state is backupRoute:
			state = primaryRoute
			switch_route(state)
	'''
	os.system('clear')

	print("SW    Num Port   Tx_Bytes   Tx_Bits/s")
	print("--------------------------------------")
	print('1     2          ' + str(round(totalTxBytes/B_to_MB, 2)) + 'MB        ' + str(round(currentTxBytes/B_to_MB*8, 2)) + 'Mbit/s')
	print('1     3          ' + str(round(totalTxBytesBckp/B_to_MB, 2)) + 'MB        ' + str(round(currentTxBytesBckp/B_to_MB*8, 2)) + 'Mbit/s')
	time.sleep(1)
