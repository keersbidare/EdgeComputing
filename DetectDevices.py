from scapy.all import *
import SendPacket
known_devices = {}
class Device:
    def __init__(self,ip='',mac=''):
        self.ip = ip
        self.mac= mac
def arp_scan(ip):
    request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip)
    ans, uans = srp(request,timeout=2,retry=2)
    detected_devices = []
    for sent, rece in ans:
        detected_devices.append(Device(ip=rece.psrc,mac=rece.hwsrc))
    #current_devices(detected_devices)
    print("*****************Detected devices*****************")
    for i in detected_devices:
        print("IP=",i.ip,"Mac=",i.mac)
    print("**************************************************")
    current_devices(detected_devices)

def current_devices(detected_devices):
    new_devices = []
    for device in detected_devices:
        if device.ip not in known_devices:
            new_devices.append(Device(device.ip,device.mac))
            known_devices[device.ip] = device.mac

            #call publisher code for tat userID as argument
            SendPacket.sendPacket(str(device.ip))
    print("_____________________________New Devices___________________________")
    for i in new_devices:
        print("IP=",i.ip,"Mac=",i.mac)
    print("__________________________________________________________________")

def main():
    ip = '192.168.206.0/24'
    restaurant_ip = '192.168.206.19'
    val = 3
    while val:
        arp_scan(ip)
        val-=1
if __name__ == "__main__":
    main()