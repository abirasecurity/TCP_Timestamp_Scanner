#!/usr/bin/env python3

import subprocess
import sys
import os
from datetime import datetime

# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def run_hping3(ip):
    """Run hping3 command with TCP timestamp on the specified IP and return the output."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}[+] Scanning {Colors.CYAN}{ip}{Colors.BLUE} at {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}{Colors.END}")

    try:
        # Check if running as root
        if os.geteuid() != 0:
            print(f"{Colors.YELLOW}[-] Warning: This script requires root privileges to run hping3{Colors.END}")
            print(f"{Colors.YELLOW}    Consider running with sudo{Colors.END}")

        # Command changed to use -c 1 (1 packet) instead of -c 2
        cmd = ["sudo", "hping3", "-S", "-p", "80", "--tcp-timestamp", "-V", "-c", "1", ip]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        # Even if there's 100% packet loss, the command technically succeeds
        # We'll handle this in the main function
        return stdout, stderr
    except Exception as e:
        print(f"{Colors.RED}[-] Exception while scanning {ip}: {str(e)}{Colors.END}")
        return None, None

def main():
    # Check if input file is provided
    if len(sys.argv) != 2:
        print(f"{Colors.YELLOW}Usage: sudo python3 tcp_ts_scanner.py <ip_list_file>{Colors.END}")
        sys.exit(1)

    ip_file = sys.argv[1]

    # Check if file exists
    if not os.path.isfile(ip_file):
        print(f"{Colors.RED}[-] Error: File '{ip_file}' not found{Colors.END}")
        sys.exit(1)

    # Read IPs from file
    try:
        with open(ip_file, 'r') as f:
            ips = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{Colors.RED}[-] Error reading IP file: {str(e)}{Colors.END}")
        sys.exit(1)

    if not ips:
        print(f"{Colors.RED}[-] No valid IPs found in the input file{Colors.END}")
        sys.exit(1)

    print(f"{Colors.GREEN}[+] Loaded {len(ips)} IP addresses from {ip_file}{Colors.END}")

    # Process each IP
    for ip in ips:
        stdout, stderr = run_hping3(ip)

        # Handle the case where we get output (even if it's packet loss)
        if stdout is not None:
            # Print the complete original output
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Complete hping3 Output ---{Colors.END}")
            print(stdout)
            if stderr:
                print(stderr)
            print(f"{Colors.MAGENTA}--------------------{Colors.END}")

            # Extract and highlight timestamp information
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Extracted TIMESTAMP Information ---{Colors.END}")
            timestamp_found = False
            for line in stdout.splitlines():
                # Look for TCP timestamp information
                if "TCP timestamp" in line:
                    print(f"{Colors.CYAN}{line.strip()}{Colors.END}")
                    timestamp_found = True

            if timestamp_found:
                print(f"\n{Colors.BOLD}{Colors.CYAN}{ip} - {Colors.RED}VULNERABLE{Colors.END}")
            else:
                # Check if we had packet loss
                if "0 packets received" in stdout or "100% packet loss" in stdout:
                    print(f"{Colors.YELLOW}No response received from target{Colors.END}")
                else:
                    print(f"{Colors.YELLOW}No TCP timestamp information found in the response{Colors.END}")

                # In either case, mark as NOT VULNERABLE
                print(f"\n{Colors.BOLD}{Colors.CYAN}{ip} - {Colors.GREEN}NOT VULNERABLE{Colors.END}")

            print(f"{Colors.MAGENTA}--------------------{Colors.END}")

if __name__ == "__main__":
    main()
