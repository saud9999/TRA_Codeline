import paramiko
from datetime import datetime

# Device list
devices = [
    {"name": "router1", "ip": "192.168.1.10", "username": "admin", "password": "admin123"},
    {"name": "router2", "ip": "192.168.1.11", "username": "admin", "password": "admin123"},
]

# Generate report filename
date_today = datetime.now().strftime("%Y-%m-%d")
report_file = f"Audit_Report_{date_today}.txt"

report_lines = []
report_lines.append("--- Network Device Audit Report ---\n")

def audit_device(device):
    findings = []

    try:
        # SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=device["ip"],
            username=device["username"],
            password=device["password"],
            timeout=5
        )

        # Commands for Cisco-style devices
        commands = {
            "telnet": "show running-config | include line vty",
            "http": "show running-config | include ip http server",
            "snmp": "show running-config | include snmp-server community"
        }

        results = {}

        for key, cmd in commands.items():
            stdin, stdout, stderr = ssh.exec_command(cmd)
            results[key] = stdout.read().decode()

        ssh.close()

        # Telnet check
        if "transport input telnet" in results["telnet"]:
            findings.append("- Telnet Status: Telnet is enabled")
        else:
            findings.append("- Telnet Status: Telnet is disabled")

        # HTTP server check
        if "ip http server" in results["http"]:
            findings.append("- HTTP Server Status: HTTP server is enabled")
        else:
            findings.append("- HTTP Server Status: HTTP server is disabled")

        # SNMP check
        if "public" in results["snmp"] or "private" in results["snmp"]:
            findings.append("- SNMP Status: Default SNMP community strings found")
        else:
            findings.append("- SNMP Status: No default SNMP community strings found")

    except Exception as e:
        findings.append(f"- Error connecting to device: {e}")

    return findings


# Audit each device
for device in devices:
    report_lines.append(f"Device: {device['name']}")

    findings = audit_device(device)

    for line in findings:
        report_lines.append(line)

    report_lines.append("")

# Save report
with open(report_file, "w") as file:
    for line in report_lines:
        file.write(line + "\n")

print(f"Audit report saved to {report_file}")