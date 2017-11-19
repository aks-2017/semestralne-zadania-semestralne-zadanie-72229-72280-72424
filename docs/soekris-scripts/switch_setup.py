import argparse
from IPy import IP

parser =  argparse.ArgumentParser(description='Set basic parameters for open vSwitch OF feature.')
group = parser.add_argument_group('Set static IP address to management interface')
group.add_argument('-a', '--address', action='store', dest='ipAdress', help="set static IP address")
group.add_argument('-m', '--mask', action='store', dest='mask', help="set network mask")
group.add_argument('-g', '--gateway', action='store', dest='gateway', help="set default gateway")

args = parser.parse_args()
ip = None
ip = IP(args.ipAdress)
mask = None
if args.mask is not None:
	mask = IP(args.mask)

if ip is not None:
	if mask is not None:
		print mask
	else:
		print "Bad mask"
	print ip
else:
	print "Invalid IP adress."
