from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException
import datetime
import os

# List of network devices
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.1",
        "username": "admin",
        "password": "admin123"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.2",
        "username": "admin",
        "password": "admin123"
    },
    {
        "device_type": "cisco_ios",
        "ip": "10.0.0.1",
        "username": "admin",
        "password": "admin123"
    },
    {
        "device_type": "juniper_junos",
        "ip": "192.168.1.3",
        "username": "admin",
        "password": "admin123"
    }
]

# Create backup directory
backup_dir = "./backups"
os.makedirs(backup_dir, exist_ok=True)

# Current date
current_date = datetime.date.today().strftime("%Y-%m-%d")

for device in devices:
    ip = device["ip"]
    device_type = device["device_type"]
    net_connect = None

    print(f"\nAttempting to connect to {ip} ({device_type})...")

    try:
        # Connect to device
        net_connect = ConnectHandler(**device)
        print(f"Successfully connected to {ip}.")

        # Get hostname
        hostname = net_connect.find_prompt().strip("#>")
        print(f"Device Hostname: {hostname}")

        # Get running config command depending on device
        if device_type == "cisco_ios":
            command = "show running-config"
        elif device_type == "juniper_junos":
            command = "show configuration"
        else:
            command = "show running-config"

        print(f"Retrieving running configuration from {hostname}...")

        config = net_connect.send_command(command)

        # Create filename
        filename = f"{hostname}_{current_date}.txt"
        filepath = os.path.join(backup_dir, filename)

        # Write config to file
        with open(filepath, "w") as file:
            file.write(config)

        print(f"Configuration backup for {hostname} saved to {filepath} successfully.")

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Error backing up configuration for {ip}: {str(e)}")

    except Exception as e:
        print(f"Unexpected error with {ip}: {str(e)}")

    finally:
        if net_connect:
            net_connect.disconnect()
        print(f"Disconnected from {ip}.")