#!/usr/bin/env python3
import argparse
from scan import scan_devices  # Import the dynamic scan function
from limit import limit_bandwidth
from block import block_device, unblock_device
from monitor import monitor_data_usage  # Import the monitor function

def main():
    parser = argparse.ArgumentParser(description="NetLimiter x: Scan, Monitor, Limit, and Block devices on your network.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Scan
    scan_parser = subparsers.add_parser("scan", help="Scan devices on the network")

    # Limit
    limit_parser = subparsers.add_parser("limit", help="Limit bandwidth for a device")
    limit_parser.add_argument("--ip", required=True, help="IP address of the target device")
    limit_parser.add_argument("--rate", required=True, help="Bandwidth limit (e.g., 500kbit or 1mbit)")
    limit_parser.add_argument("--direction", required=True, choices=["download", "upload"], help="Direction to limit: 'download' or 'upload'")

    # Block
    block_parser = subparsers.add_parser("block", help="Block a device")
    block_parser.add_argument("--ip", required=True, help="IP address of the target device")

    # Unblock
    unblock_parser = subparsers.add_parser("unblock", help="Unblock a device")
    unblock_parser.add_argument("--ip", required=True, help="IP address of the target device")

    # Monitor
    monitor_parser = subparsers.add_parser("monitor", help="Monitor data usage for a device")
    monitor_parser.add_argument("--id", required=True, type=int, help="Device ID to monitor")
    monitor_parser.add_argument("--direction", choices=["upload", "download"], help="Direction of data usage to monitor ('upload' or 'download')")
    monitor_parser.add_argument("--duration", type=int, help="Duration to monitor in seconds (default is 60)")

    args = parser.parse_args()

    if args.command == "scan":
        scan_devices(silent=False)  # Dynamically scan the devices and print them
    elif args.command == "limit":
        limit_bandwidth(args.ip, args.rate, args.direction)
    elif args.command == "block":
        block_device(args.ip)
    elif args.command == "unblock":
        unblock_device(args.ip)
    elif args.command == "monitor":
        # Use default values if direction or duration is not provided
        direction = args.direction if args.direction else None
        duration = args.duration if args.duration else 60

        # Monitor based on device ID, direction, and duration
        monitor_data_usage(args.id, direction, duration)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

