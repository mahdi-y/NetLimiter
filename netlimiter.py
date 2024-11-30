#!/usr/bin/env python3
import argparse
from scan import scan_devices
from limit import limit_bandwidth
from block import block_device, unblock_device
from monitor import monitor_data_usage

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
    monitor_parser.add_argument("--ip", required=True, help="IP address of the device to monitor")
    monitor_parser.add_argument("--direction", required=True, choices=["upload", "download"], help="Direction to monitor: 'upload' or 'download'")
    monitor_parser.add_argument("--duration", required=True, type=int, help="Duration to monitor (in seconds)")	

    args = parser.parse_args()

    if args.command == "scan":
        scan_devices()
    elif args.command == "limit":
        limit_bandwidth(args.ip, args.rate, args.direction)
    elif args.command == "block":
        block_device(args.ip)
    elif args.command == "unblock":
        unblock_device(args.ip)
    elif args.command == "monitor":
        monitor_data_usage(args.ip, args.direction, args.duration)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
