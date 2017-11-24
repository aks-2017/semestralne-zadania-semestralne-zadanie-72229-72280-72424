import requests
import json
import configparser
import time

upperThreshold = 0.5
lowerThreshold = 0.3
primaryRoute = 0
backupRoute = 1
max_speed = 10485760

state = primaryRoute

class Router(object):
	def __init__(self,j):
		self.__dict__ = j.json()[0]

def getPortStatsInfo():
	r = requests.get(cntrllr_url + '/stats/port/1/3')
	print(r.status_code)
	h = r.json()['1'][0]['tx_bytes']
	print('D: ' + str(h))
	return h	

def switchRoute(route):
	url_sw1 = cntrllr_url + '/router/0000000000000001'
	url_sw3 = cntrllr_url + '/router/0000000000000003' 
	add_dst_sw1 = config['SW1-route']['dst1']
	add_dst_sw3 = config['SW3-route']['dst1']
	print('D1')
	if route is primaryRoute:
	   	gateway = config['SW1-route']['gateway1']
	   	payload = {'destination': add_dst_sw1, 'gateway': gateway}
	   	r = requests.post(url_sw1, data=json.dumps(payload))
		
		if r.status_code is 200:
			print("Changed route to primary on SW1.")
		
		gateway = config['SW3-route']['gateway1']
                payload = {'destination': add_dst_sw3, 'gateway': gateway}
                r = requests.post(url, data=json.dumps(payload))

                if r.status_code is 200:
                        print("Changed route to primary on SW3.")		

	if route is backupRoute:
		gateway = config['SW1-route']['bckpgateway']
                payload = {'destination': add_dst_sw1, 'gateway': gateway}
                r = requests.post(url, data=json.dumps(payload)) 
		
		if r.status_code is 200:
                        print("Changed route to backup on SW1.")
	
		gateway = config['SW3-route']['bckpgateway']
                payload = {'destination': add_dst_sw3, 'gateway': gateway}
                r = requests.post(url, data=json.dumps(payload))

                if r.status_code is 200:
                        print("Changed route to backup on SW3.")

	
def sw_conf(sw_id):
	sw = "SW" + sw_id + "-add"
	url = cntrllr_url + '/router/000000000000000' + sw_id

	for ip in config[sw]['address'].split(','):
		payload = {'address': ip}
		r = requests.post(url, data=json.dumps(payload))

	sw = "SW" + sw_id + "-route"

	payload = {}
	
	for item in config[sw]:
		if 'dst' in item:
			payload['destination'] = config[sw][item]

		
		if 'gateway' in item:	
			payload['gateway'] = config[sw][item]
			r = requests.post(url, data=json.dumps(payload))
			print(r.status_code)
			payload = {}



try:
	config = configparser.ConfigParser()
	config.read('config')
except Error as e:
	print("Error read config file: " + e )

cntrllr_url = config['Controller']['url']

sw_conf('1')
sw_conf('2')
sw_conf('3')


totalTxBytes = getPortStatsInfo() 
i=0

while True:
	i += 1
	oldTxBytes = totalTxBytes
	totalTxBytes = getPortStatsInfo()
	
	if totalTxBytes != oldTxBytes:
		if (totalTxBytes - oldTxBytes) > (max_speed * upperThreshold) and state is primaryRoute:
			state = backupRoute
			switchRoute(state)
		
		if (totalTxBytes - oldTxBytes) < (max_speed * lowerThreshold) and state is backupRoute:
			state = primaryRoute
                        switchRoute(state)

#	print(getPortStatsInfo())
	print(i)
	time.sleep(1)
