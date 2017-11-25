import argparse
from IPy import IP
import subprocess

def main():
	args = argsSetUp()
	if (args.ipAdress is not None) and (args.mask is not None):
		setIP(args.ipAdress, args.mask, args.gateway)
	elif (args.contrIpAddress is not None):
		setControllerAddress(args.contrIpAddress)
	elif (args.gateway is not None):
		setGateway(args.gateway)
	else:
		print "No parameter selected."

#set all needed arguments to parser
def argsSetUp():
        examples = '''Examples:
 python switch_setup.py -a 192.168.0.25 -m 255.255.255.0 -g 192.168.0.1		set IP address with gateway
 python switch_setup.py -a 192.168.0.25 -m 255.255.255.0			set only IP address
 python switch_setup.py -g 192.168.0.1						set only gateway
 python switch_setup.py -c 192.168.0.100:6633					set controller address
 '''
	
	parser = argparse.ArgumentParser(prog='base_maker', description='Set basic parameters for open vSwitch OF feature.', epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
	
	parser.add_argument('-c', '--controller', action='store', dest='contrIpAddress', help='Set SDN controller IP address and port (Format: X.X.X.X:Port).')
	
	group = parser.add_argument_group('Set static IP address to management interface')
	group.add_argument('-a', '--address', action='store', dest='ipAdress', help="set static IP address")
	group.add_argument('-m', '--mask', action='store', dest='mask', help="set network mask")
	group.add_argument('-g', '--gateway', action='store', dest='gateway', help="set default gateway")
	
	return parser.parse_args()

#set IP address and mask on enp5s0 interface
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
	if(gatewayRaw is not None):
		try:
			gateway = IP(gatewayRaw)
		except ValueError:
			print "Invalid gateway format."
			return
		try:
			subprocess.call(['ifconfig', 'enp5s0', ipAddress, 'netmask', maskRaw])
			subprocess.call(['ip', 'route', 'del', 'default'])
			subprocess.call(['ip', 'route', 'add', 'default', 'via', gatewayRaw])
		except subprocess.CalledProcessError:
			print subprocess.CalledProcessError.output
	else:
		try:
                        subprocess.call(['ifconfig', 'enp5s0', ipAddress, 'netmask', maskRaw])
		except subprocess.CalledProcessError:
			print subprocess.CalledProcessError.output

#set gateway on enp5s0 interface
def setGateway(gatewayRaw):
	try:
		gateway = IP(gatewayRaw)
	except ValueError:
		print "Invalid gateway format."
                return
        try:
		subprocess.call(['ip', 'route', 'del', 'default'])
		subprocess.call(['ip', 'route', 'add', 'default', 'via', gatewayRaw])
      	except subprocess.CalledProcessError:
        	print subprocess.CalledProcessError.output

#set controller address and port in OVS
def setControllerAddress(controllerIP):
	try:
		subprocess.call(['ovs-vsctl', 'set-controller', 'of-switch', 'tcp:' + controllerIP])
	except subprocess.CalledProcessError:
                print subprocess.CalledProcessError.output

if __name__ == '__main__':
	main()
