#!/usr/bin/env python3

import subprocess
import sys
import os
from datetime import datetime

def run_hping3(ip):
    """Run hping3 command with TCP timestamp on the specified IP and return the output."""
    print(f"\n[+] Scanning {ip} at {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")

    try:
        # Check if running as root
        if os.geteuid() != 0:
            print("[-] Warning: This script requires root privileges to run hping3")
            print("    Consider running with sudo")

        # Command as specified: sudo hping3 -S -p 80 --tcp-timestamp -V -c 2 IP
        cmd = ["sudo", "hping3", "-S", "-p", "80", "--tcp-timestamp", "-V", "-c", "2", ip]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        # Check for errors
        if process.returncode != 0:
            print(f"[-] Error scanning {ip}: {stderr}")
            return None

        return stdout
    except Exception as e:
        print(f"[-] Exception while scanning {ip}: {str(e)}")
        return None

def main():
    # Check if input file is provided
    if len(sys.argv) != 2:
        print("Usage: sudo python3 tcp_ts_scanner.py <ip_list_file>")
        sys.exit(1)

    ip_file = sys.argv[1]

    # Check if file exists
    if not os.path.isfile(ip_file):
        print(f"[-] Error: File '{ip_file}' not found")
        sys.exit(1)

    # Read IPs from file
    try:
        with open(ip_file, 'r') as f:
            ips = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Error reading IP file: {str(e)}")
        sys.exit(1)

    if not ips:
        print("[-] No valid IPs found in the input file")
        sys.exit(1)

    print(f"[+] Loaded {len(ips)} IP addresses from {ip_file}")

    # Process each IP
    for ip in ips:
        output = run_hping3(ip)
        if output:
            # Print the complete original output
            print("\n--- Complete hping3 Output ---")
            print(output)
            print("--------------------")

            # Extract and highlight timestamp information
            print("\n--- Extracted TIMESTAMP Information ---")
            timestamp_found = False
            for line in output.splitlines():
                # Look for TCP timestamp information
                if "TCP timestamp" in line:
                    print(f"{line.strip()}")
                    timestamp_found = True

            if not timestamp_found:
                print("No TCP timestamp information found in the response")
            print("--------------------")

if __name__ == "__main__":
    main()
