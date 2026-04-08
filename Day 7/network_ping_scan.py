import subprocess
import json
import yaml
import smtplib
from datetime import datetime
from email.message import EmailMessage

# Network range to scan
network_prefix = "192.168.1."
hosts = range(1, 255)

# Gmail configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
gmail_user = "your_email@gmail.com"
gmail_password = "your_app_password"
receiver_email = "receiver_email@gmail.com"

# Scan results
results = []

print("Starting network scan...")

for host in hosts:
    ip = f"{network_prefix}{host}"

    try:
        response = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL
        )

        status = "UP" if response.returncode == 0 else "DOWN"

        results.append({
            "ip": ip,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        results.append({
            "ip": ip,
            "status": "ERROR",
            "error": str(e)
        })

print("Scan completed.")

# Save JSON report
json_file = "network_report.json"
with open(json_file, "w") as f:
    json.dump(results, f, indent=4)

# Save YAML report
yaml_file = "network_report.yaml"
with open(yaml_file, "w") as f:
    yaml.dump(results, f)

print("Reports saved.")

# Send email
msg = EmailMessage()
msg["Subject"] = "Network Ping Scan Report"
msg["From"] = gmail_user
msg["To"] = receiver_email
msg.set_content("Attached is the latest network scan report.")

# Attach JSON file
with open(json_file, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="json",
        filename=json_file
    )

# Attach YAML file
with open(yaml_file, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="yaml",
        filename=yaml_file
    )

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)

    print("Email sent successfully.")

except Exception as e:
    print("Failed to send email:", e)