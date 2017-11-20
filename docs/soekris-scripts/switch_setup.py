import argparse
from IPy import IP
import subprocess

def main():
	args = argsSetUp()
	if (args.ipAdress is not None) and (args.mask is not None) and (args.gateway is not None):
		setIP(args.ipAdress, args.mask, args.gateway)
	else:
		print "No parameter selected."

def argsSetUp():
	parser =  argparse.ArgumentParser(description='Set basic parameters for open vSwitch OF feature.')
	group = parser.add_argument_group('Set static IP address to management interface')
	group.add_argument('-a', '--address', action='store', dest='ipAdress', help="set static IP address")
	group.add_argument('-m', '--mask', action='store', dest='mask', help="set network mask")
	group.add_argument('-g', '--gateway', action='store', dest='gateway', help="set default gateway")
	return parser.parse_args()

def setIP(ipAddress, maskRaw, gatewayRaw):
	try:
		ip = IP(ipAddress)
	except ValueError:
		print "Invalid IP address format."
		return
	try:
		mask = IP(maskRaw)
	except ValueError:
		print "Invalid mask format."
		return
	try:
		gateway = IP(gatewayRaw)
	except ValueError:
		print "Invalid gateway format."
		return
	try:
		subprocess.call(['ifconfig', 'enp5s0', ipAddress, 'netmask', maskRaw])
		subprocess.call(['ip', 'route', 'add', 'default', 'via', gatewayRaw])
	except subprocess.CalledProcessError:
		print subprocess.CalledProcessError.output

if __name__ == '__main__':
	main()
