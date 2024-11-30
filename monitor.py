from scapy.all import sniff, IP
import time
from scan import scan_devices  # Import scan_devices to dynamically load devices

def get_device_ip_by_id(device_id):
    """Fetch the IP address for a given device ID from the dynamically loaded device list."""
    devices = scan_devices(silent=True)  # Dynamically fetch devices without printing
    devices_sorted = sorted(devices, key=lambda x: x["ip"])  # Sort devices by IP for consistency
    for device in devices_sorted:
        if device["id"] == device_id:
            return device["ip"]
    return None

def monitor_data_usage(device_id, direction=None, duration=60):
    """
    Monitor data usage for a device based on ID (not IP), direction ('upload' or 'download'), and duration (in seconds).
    If direction or duration is not specified, defaults are applied.
    """
    ip_address = get_device_ip_by_id(device_id)

    if not ip_address:
        print(f"Device with ID {device_id} not found.")
        return

    data_usage_upload = 0
    data_usage_download = 0

    def packet_callback(pkt):
        nonlocal data_usage_upload, data_usage_download
        if pkt.haslayer(IP) and pkt[IP].src == ip_address:
            data_usage_upload += len(pkt)  # Counting the packet size for upload
        elif pkt.haslayer(IP) and pkt[IP].dst == ip_address:
            data_usage_download += len(pkt)  # Counting the packet size for download

    print(f"Monitoring traffic for IP {ip_address} (Device ID {device_id}) for {duration} seconds...")

    # If no direction is specified, monitor both upload and download
    if direction is None:
        print("Monitoring both upload and download traffic.")
        sniff(prn=packet_callback, timeout=duration, store=False)
        # Convert the data usage from bytes to Kbits/Mbits for both directions
        data_usage_kbits_upload = (data_usage_upload * 8) / 1024
        data_usage_mbits_upload = data_usage_kbits_upload / 1024
        data_usage_kbits_download = (data_usage_download * 8) / 1024
        data_usage_mbits_download = data_usage_kbits_download / 1024

        # Output the data usage for both directions
        if data_usage_mbits_upload > 1:
            print(f"Total upload data usage for Device ID {device_id} (IP {ip_address}): {data_usage_mbits_upload:.2f} Mbit")
        else:
            print(f"Total upload data usage for Device ID {device_id} (IP {ip_address}): {data_usage_kbits_upload:.2f} Kbit")

        if data_usage_mbits_download > 1:
            print(f"Total download data usage for Device ID {device_id} (IP {ip_address}): {data_usage_mbits_download:.2f} Mbit")
        else:
            print(f"Total download data usage for Device ID {device_id} (IP {ip_address}): {data_usage_kbits_download:.2f} Kbit")

    else:
        # Monitor only the specified direction (upload or download)
        print(f"Monitoring {direction} traffic.")
        sniff(prn=packet_callback, timeout=duration, store=False)

        # Convert the data usage from bytes to Kbits/Mbits
        if direction == "upload":
            data_usage_kbits = (data_usage_upload * 8) / 1024
            data_usage_mbits = data_usage_kbits / 1024
            if data_usage_mbits > 1:
                print(f"Total upload data usage for Device ID {device_id} (IP {ip_address}): {data_usage_mbits:.2f} Mbit")
            else:
                print(f"Total upload data usage for Device ID {device_id} (IP {ip_address}): {data_usage_kbits:.2f} Kbit")
        elif direction == "download":
            data_usage_kbits = (data_usage_download * 8) / 1024
            data_usage_mbits = data_usage_kbits / 1024
            if data_usage_mbits > 1:
                print(f"Total download data usage for Device ID {device_id} (IP {ip_address}): {data_usage_mbits:.2f} Mbit")
            else:
                print(f"Total download data usage for Device ID {device_id} (IP {ip_address}): {data_usage_kbits:.2f} Kbit")
