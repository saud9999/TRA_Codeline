import paramiko
from datetime import datetime

# Device list
devices = [
    {"name": "router1", "ip": "192.168.1.10", "username": "admin", "password": "admin123"},
    {"name": "router2", "ip": "192.168.1.11", "username": "admin", "password": "admin123"},
]

# Create report file with date
date_today = datetime.now().strftime("%Y-%m-%d")
report_file = f"Audit_Report_{date_today}.txt"

report_lines = []
report_lines.append("--- Network Device Audit Report ---\n")


def run_command(ssh, command):
    """Execute command and return clean output"""
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode().strip()


def audit_device(device):

    findings = []

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=device["ip"],
            username=device["username"],
            password=device["password"],
            timeout=10,
            banner_timeout=10
        )

        # Run commands
        telnet_output = run_command(ssh, "show running-config | section line vty")
        http_output = run_command(ssh, "show running-config | include ip http")
        snmp_output = run_command(ssh, "show running-config | include snmp-server community")

        ssh.close()

        # TELNET CHECK
        if "transport input telnet" in telnet_output or "transport input all" in telnet_output:
            findings.append("- Telnet Status: Telnet is enabled (INSECURE)")
        else:
            findings.append("- Telnet Status: Telnet is disabled")

        # HTTP SERVER CHECK
        if "ip http server" in http_output and "no ip http server" not in http_output:
            findings.append("- HTTP Server Status: HTTP server is enabled (INSECURE)")
        else:
            findings.append("- HTTP Server Status: HTTP server is disabled")

        # SNMP DEFAULT COMMUNITY CHECK
        if "public" in snmp_output.lower() or "private" in snmp_output.lower():
            findings.append("- SNMP Status: Default SNMP community strings found (INSECURE)")
        else:
            findings.append("- SNMP Status: No default SNMP community strings found")

    except paramiko.AuthenticationException:
        findings.append("- ERROR: Authentication failed")

    except paramiko.SSHException:
        findings.append("- ERROR: SSH connection issue")

    except Exception as e:
        findings.append(f"- ERROR: {str(e)}")

    return findings


# Audit devices
for device in devices:

    report_lines.append(f"Device: {device['name']}")
    report_lines.append(f"IP Address: {device['ip']}")

    findings = audit_device(device)

    for line in findings:
        report_lines.append(line)

    report_lines.append("")


# Write report
with open(report_file, "w") as f:
    f.write("\n".join(report_lines))

print(f"Audit report saved to {report_file}")