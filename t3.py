import re
import csv
import json
from collections import Counter
from datetime import datetime

log_file = "firewall.log"

parsed_entries = []
malformed_count = 0
total_entries = 0

action_counter = Counter()
port_counter = Counter()
source_counter = Counter()

# Regex pattern for valid log entry
pattern = re.compile(
    r'(\d{4}\s-\s\d{2}\s-\s\d{2}\s\d{2}:\d{2}:\d{2})\s'
    r'(ACCEPT|DROP)\s'
    r'(TCP|UDP|ICMP)\s'
    r'SRC=(\d+\.\d+\.\d+\.\d+)\s'
    r'SPT=(\d+)\s'
    r'DST=(\d+\.\d+\.\d+\.\d+)\s'
    r'DPT=(\d+)\s'
    r'LEN=(\d+)'
)

with open(log_file, "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        total_entries += 1
        match = pattern.search(line)

        if match:
            data = {
                "timestamp": match.group(1),
                "action": match.group(2),
                "protocol": match.group(3),
                "source_ip": match.group(4),
                "source_port": match.group(5),
                "destination_ip": match.group(6),
                "destination_port": match.group(7),
                "packet_size": match.group(8)
            }

            parsed_entries.append(data)

            action_counter[data["action"]] += 1
            port_counter[data["destination_port"]] += 1
            source_counter[data["source_ip"]] += 1

        else:
            malformed_count += 1


# Identify suspicious IPs
suspicious_ips = {ip: count for ip, count in source_counter.items() if count >= 3}

# Top 3 targeted ports
top_ports = port_counter.most_common(3)

# -----------------------------
# Save CSV
# -----------------------------
with open("output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow([
        "Timestamp",
        "Action",
        "Protocol",
        "Source IP",
        "Source Port",
        "Destination IP",
        "Destination Port",
        "Packet Size"
    ])

    for entry in parsed_entries:
        writer.writerow([
            entry["timestamp"],
            entry["action"],
            entry["protocol"],
            entry["source_ip"],
            entry["source_port"],
            entry["destination_ip"],
            entry["destination_port"],
            entry["packet_size"]
        ])

# -----------------------------
# Save JSON
# -----------------------------
with open("output.json", "w") as jsonfile:
    json.dump(parsed_entries, jsonfile, indent=4)

# -----------------------------
# Save Threat Report
# -----------------------------
with open("threats.txt", "w") as threat_file:

    threat_file.write("THREAT REPORT - Generated : " +
                      datetime.now().strftime("%Y - %m - %d %H : %M : %S") + "\n")

    threat_file.write("================================================\n")
    threat_file.write("Suspicious IPs (3+ log appearances):\n")

    for ip, count in suspicious_ips.items():
        threat_file.write(f"IP : {ip} | Occurrences : {count}\n")


# -----------------------------
# Terminal Report
# -----------------------------
print("=" * 60)
print("FIREWALL LOG ANALYSIS REPORT")
print("=" * 60)

print(f"Total entries processed : {total_entries}")
print(f"Valid entries parsed : {len(parsed_entries)}")
print(f"Malformed entries skipped: {malformed_count}")

print("\n--- Action Summary ---")
for action, count in action_counter.items():
    print(f"{action} : {count}")

print("\n--- Top 3 Targeted Destination Ports ---")
for i, (port, count) in enumerate(top_ports, start=1):
    print(f"{i}. Port {port} — {count} hits")

print("\n--- Suspicious Source IPs (3+ appearances) ---")
for ip, count in suspicious_ips.items():
    print(f"{ip} — {count} occurrences")

print("\nOutput saved:")
print("output.csv")
print("output.json")
print("threats.txt")

print("=" * 60)