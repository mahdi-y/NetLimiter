from scapy.all import sniff, IP
import time

def monitor_data_usage(ip, direction, duration):
    """
    Monitor data usage for the given IP address for a certain duration.
    direction can be 'upload' or 'download'.
    """
    data_usage = 0

    def packet_callback(pkt):
        nonlocal data_usage
        if pkt.haslayer(IP) and pkt[IP].src == ip:
            if direction == "upload":
                data_usage += len(pkt)  # Counting the packet size
        elif pkt.haslayer(IP) and pkt[IP].dst == ip:
            if direction == "download":
                data_usage += len(pkt)  # Counting the packet size

    print(f"Monitoring {direction} traffic for IP {ip} for {duration} seconds...")
    start_time = time.time()

    sniff(prn=packet_callback, timeout=duration, store=False)

    # Convert the data usage from bytes to Kbits/Mbits
    data_usage_kbits = (data_usage * 8) / 1024  # Convert to Kbits
    data_usage_mbits = data_usage_kbits / 1024  # Convert to Mbits

    if data_usage_mbits > 1:
        print(f"Total {direction} data usage for IP {ip}: {data_usage_mbits:.2f} Mbit")
    else:
        print(f"Total {direction} data usage for IP {ip}: {data_usage_kbits:.2f} Kbit")
