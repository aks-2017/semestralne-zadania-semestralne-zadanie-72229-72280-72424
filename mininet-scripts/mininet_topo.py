from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.node import RemoteController
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from subprocess import Popen, PIPE, STDOUT

class SimplePktSwitch(Topo):
    def __init__(self, **opts):
        """Create custom topo."""
        # Initialize topology
        # It uses the constructor for the Topo cloass
        super(SimplePktSwitch, self).__init__(**opts)

        # Add hosts and switches
        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1/24")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2/24")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.0.0.3/24")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="10.0.0.4/24")

        # Adding switches
        s1 = self.addSwitch('s1', dpid="1")
        s2 = self.addSwitch('s2', dpid="2")
        s3 = self.addSwitch('s3', dpid="3")

        # Add links
        self.addLink(h1, s1, 0, 1, bw=100)
        self.addLink(h2, s1, 0, 2, bw=100)
        self.addLink(h3, s3, 0, 1, bw=100)
        self.addLink(h4, s3, 0, 2, bw=100)

        self.addLink(s1, s2, 3, 1, bw=100)
        self.addLink(s2, s3, 2, 3, bw=100)
        self.addLink(s1, s3, 4, 4, bw=100)


#topos = { 'mytopo': ( lambda: SimplePktSwitch() ) }

def run():
    c = RemoteController('c', '127.0.0.1', 6633)
    net = Mininet(topo=SimplePktSwitch(), host=CPULimitedHost, link=TCLink, controller=c)
    net.start()
  	
    sw = net.get('s1')
    sw.cmd('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    sw = net.get('s2')
    sw.cmd('ovs-vsctl set Bridge s2 protocols=OpenFlow13')
    sw = net.get('s3')
    sw.cmd('ovs-vsctl set Bridge s3 protocols=OpenFlow13')
	
    cmd = ['ryu-manager ryu.app.ofctl_rest ryu.app.simple_switch_13']
    p = Popen(cmd, shell= True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    if p.poll() == None:
        print ("Ryu and Ryu.apps are running.") 
    else:
        print ("Ryu and Ryu.apps are not running.")
    
    CLI(net)
    net.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()
