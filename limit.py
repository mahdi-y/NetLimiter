import os
from utils import setup_ifb

def limit_bandwidth(ip, rate, direction):
    interface = "eth0"  # Replace with your interface
    if direction == "upload":
        # Limit outbound (upload) traffic
        os.system(f"tc qdisc add dev {interface} root handle 1: htb default 12")
        os.system(f"tc class add dev {interface} parent 1: classid 1:12 htb rate {rate}")
        os.system(f"tc filter add dev {interface} protocol ip parent 1:0 prio 1 u32 match ip src {ip} flowid 1:12")
        print(f"Upload bandwidth for {ip} limited to {rate}")
    elif direction == "download":
        # Limit inbound (download) traffic
        setup_ifb(interface)
        os.system(f"tc qdisc add dev ifb0 root handle 1: htb default 12")
        os.system(f"tc class add dev ifb0 parent 1: classid 1:12 htb rate {rate}")
        os.system(f"tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip dst {ip} flowid 1:12")
        print(f"Download bandwidth for {ip} limited to {rate}")
    else:
        print("Invalid direction. Use 'download' or 'upload'.")
