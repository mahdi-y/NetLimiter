import os

def block_device(ip):
    os.system(f"iptables -A FORWARD -s {ip} -j DROP")
    print(f"Blocked {ip}")

def unblock_device(ip):
    os.system(f"iptables -D FORWARD -s {ip} -j DROP")
    print(f"Unblocked {ip}")
