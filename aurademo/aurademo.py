import os

class setup(object):
    def __init__(self,options,cfg):
        self.options = options
        self.cfg = cfg

    def Bootfile(self):
        cfg = self.cfg
   
        buf = """#/bin/env bash
####### aurademo generated setupscript for gwc c7 vm

### sshd
sed -i 's,#UseDNS yes,UseDNS no,' /etc/ssh/sshd_config
systemctl restart sshd.service

### IP forwarding
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward = 1" > /etc/sysctl.d/98-ipforwarding.conf

### packages
yum install -y epel-release
yum install -y iperf screen ntpdate ntp bind-utils tcpdump telnet openvpn dnsmasq

### dnsmasq setup
echo "conf-dir=/etc/dnsmasq.d,.rpmnew,.rpmsave,.rpmorig" > /etc/dnsmasq.conf
echo "addn-hosts=/etc/demo_hosts" >> /etc/dnsmasq.conf
touch /etc/demo_hosts

### services
# ntpd
systemctl enable ntpd
systemctl start ntpd
systemctl status ntpd

#dnsmasq
systemctl enable dnsmasq
systemctl start dnsmasq
systemctl status dnsmasq

#### setup to connect with gwsvpn
base64 --decode > /etc/openvpn/gwsvpn.conf <<__EOF__

%(vpnbuf)s

__EOF__
#make SELinux disable persistent
echo "SELINUX=disabled" > /etc/selinux/config
setenforce 0
systemctl enable openvpn@gwsvpn
systemctl start openvpn@gwsvpn
systemctl status openvpn@gwsvpn


###

""" % cfg
        return buf
        
    def Vagrantfile(self):
        cfg = self.cfg

        buf = ''

        for o in cfg["__ordered__"]:
            options=cfg[o]
            buf = buf + """
# %(__name__)s 
Vagrant.configure("2") do |%(__name__)sconfig|
  %(__name__)sconfig.vm.define "%(__name__)s" do |%(__name__)s|
    %(__name__)s.vm.provision "shell", path: "%(setupscript)s"
    %(__name__)s.vm.box = "%(box)s"
    %(network)s
    %(__name__)s.vm.provider "virtualbox" do |vb|
        vb.gui = true
        vb.memory = "%(memory)s"
    end
  end
end
""" % options
        return buf

    def runner(self):
        with open(os.path.join(self.options.workdir,"Vagrantfile"),"w") as f:
            f.write(self.Vagrantfile())
        with open(os.path.join(self.options.workdir,"gwcsetupscript.sh"),"w") as f:
            f.write(self.Bootfile())

def main(options, cfg):
    s = setup(options,cfg)
    s.runner()
