# TCP_Timestamp_Scanner
A Python utility for scanning multiple IP addresses with TCP timestamp requests using hping3.

## Overview

This tool automates the process of sending TCP SYN packets with timestamp options to a list of IP addresses and extracting the timestamp information from the responses. It uses the `hping3` utility to perform the scans and provides both the complete output and the extracted timestamp information.

## Features

- Reads IP addresses from a text file
- Sends TCP SYN packets with timestamp options to port 80 of each IP
- Displays complete hping3 output
- Extracts and highlights TCP timestamp information
- Handles errors gracefully
- Provides timestamps for scan operations

## Requirements

- Python 3.6+
- hping3 installed on the system
- Root/sudo privileges (required for sending raw TCP packets)

## Installation

1. Ensure hping3 is installed:

```
# On Debian/Ubuntu
sudo apt-get install hping3

# On CentOS/RHEL
sudo yum install hping3
```

2. Clone or download this script to your system

## Usage

1. Create a text file with target IP addresses, one per line:

```
192.168.1.1
10.0.0.1
8.8.8.8
```

2. Run the script with sudo:

```
sudo python3 tcp_ts_scanner.py ip_list.txt
```

3. Review the output for each IP address

## Output Example

```
# Sample Output 1: Vulnerable Host

[+] Loaded 3 IP addresses from targets.txt

[+] Scanning 192.168.1.1 at 2025-05-22 10:15:34 AM

--- Complete hping3 Output ---
HPING 192.168.1.1 (eth0 192.168.1.1): S set, 40 headers + 0 data bytes
len=46 ip=192.168.1.1 ttl=64 DF id=0 sport=80 flags=SA seq=0 win=5840 rtt=2.3 ms
TCP timestamp: tcpts=3845731200

--- 192.168.1.1 hping statistic ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 2.3/2.3/2.3 ms
--------------------

--- Extracted TIMESTAMP Information ---
TCP timestamp: tcpts=3845731200

192.168.1.1 - VULNERABLE
--------------------

# Sample Output 2: Non-Vulnerable Host (Responds but no timestamp)

[+] Scanning 10.0.0.25 at 2025-05-22 10:15:37 AM

--- Complete hping3 Output ---
HPING 10.0.0.25 (eth0 10.0.0.25): S set, 40 headers + 0 data bytes
len=44 ip=10.0.0.25 ttl=64 DF id=0 sport=80 flags=SA seq=0 win=65535 rtt=1.8 ms

--- 10.0.0.25 hping statistic ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 1.8/1.8/1.8 ms
--------------------

--- Extracted TIMESTAMP Information ---
No TCP timestamp information found in the response

10.0.0.25 - NOT VULNERABLE
--------------------

# Sample Output 3: Non-Vulnerable Host (No response)

[+] Scanning 50.175.72.18 at 2025-05-22 10:15:40 AM

--- Complete hping3 Output ---
HPING 50.175.72.18 (eth0 50.175.72.18): S set, 40 headers + 0 data bytes

--- 50.175.72.18 hping statistic ---
1 packets transmitted, 0 packets received, 100% packet loss
round-trip min/avg/max = 0.0/0.0/0.0 ms
--------------------

--- Extracted TIMESTAMP Information ---
No response received from target

50.175.72.18 - NOT VULNERABLE
--------------------

# Sample Output 4: Error Case

[+] Scanning 256.0.0.1 at 2025-05-22 10:15:43 AM
[-] Exception while scanning 256.0.0.1: Invalid IP address format
```

## Understanding TCP Timestamps

TCP timestamps are a TCP option defined in RFC 1323 that can provide:

1. **System Uptime Information**: The TCP timestamp value often correlates with the system uptime counter (typically incremented in milliseconds or 100ms intervals).

2. **Operating System Fingerprinting**: Different operating systems implement TCP timestamps differently, which can help identify the target OS.

3. **Network Performance Metrics**: TCP timestamps are used for Round-Trip Time Measurement (RTTM) and Protection Against Wrapped Sequences (PAWS).

The format of the extracted timestamp is:
- `tcpts=<value>`: The TCP timestamp value from the target system

## Security Implications

TCP timestamp responses can reveal information about a target system that might be useful during reconnaissance phases of penetration testing:

- System uptime (how long the system has been running)
- Operating system identification
- Network configuration details

Many security-conscious organizations configure their systems to disable TCP timestamps or randomize the values to prevent information leakage.

## Command Details

The script uses the following hping3 command:

```
sudo hping3 -S -p 80 --tcp-timestamp -V -c 2 <IP>
```

Where:
- `-S`: Sets the SYN flag in TCP packets
- `-p 80`: Targets port 80 (HTTP)
- `--tcp-timestamp`: Enables the TCP timestamp option
- `-V`: Verbose mode
- `-c 2`: Sends 2 packets

# Ethical Usage

This tool is intended for:

1. Security professionals conducting authorized penetration tests
2. Website owners testing their own sites for vulnerabilities
3. Educational purposes to understand clickjacking protections

Always obtain proper authorization before testing any website you don't own

# License
MIT License

# Contributing
Contributions are welcome! Please feel free to submit a Pull Request

