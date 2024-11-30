from scapy.all import ARP, Ether, srp
import socket
import struct

# Your network's IP range (modify this as per your network)
network_ip_range = "192.168.1.0/24"

def ip_to_int(ip):
    """Convert an IP address string to an integer."""
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def scan_network():
    print("Scanning the network...")
    # Create an ARP request packet
    arp_request = ARP(pdst=network_ip_range)
    # Create an Ethernet frame to carry the ARP request
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine the Ethernet frame and ARP request
    packet = broadcast / arp_request

    # Send the packet and capture responses
    answered, _ = srp(packet, timeout=2, verbose=False)

    # Extract IP and MAC addresses from responses
    devices = []
    for sent, received in answered:
        devices.append((received.psrc, received.hwsrc))

    return devices

def scan_devices():
    devices = scan_network()

    # Sort devices by IP address numerically
    devices.sort(key=lambda x: ip_to_int(x[0]))

    # Display devices in a table
    print("\nActive Devices on the Network:")
    print("-" * 50)
    print("{:<5} {:<20} {:<20}".format("ID", "IP Address", "MAC Address"))
    print("-" * 50)

    for idx, (ip, mac) in enumerate(devices, start=1):
        print(f"{idx:<5} {ip:<20} {mac:<20}")
    print("-" * 50)
    
    return devices

