from scapy.all import ARP, Ether, srp
import ipaddress  # Import to handle IP addresses for sorting

# Your network's IP range (modify this as per your network)
network_ip_range = "192.168.1.0/24"

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

    # Extract and store active IPs with their MAC addresses
    devices = []
    for sent, received in answered:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    # Sort devices by IP address numerically
    devices.sort(key=lambda device: ipaddress.IPv4Address(device["ip"]))

    # Assign IDs based on sorted order
    for idx, device in enumerate(devices, 1):
        device["id"] = idx

    return devices

def scan_devices(silent=False):
    """
    Scans the network for active devices and optionally suppresses the output.
    """
    devices = scan_network()

    # If silent is False, print the device information
    if not silent:
        print("\nActive Devices on the Network:")
        print("-" * 50)
        print("{:<10} {:<20} {:<20} {:<20}".format("ID", "IP Address", "MAC Address", "Status"))
        print("-" * 50)

        for device in devices:
            print("{:<10} {:<20} {:<20} Connected".format(device["id"], device["ip"], device["mac"]))

    return devices  # Return devices list for later use

