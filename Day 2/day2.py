# IP_Address = input("Enter an IP address (e.g., 192.168.1.1): ")
# cidr = input("Enter CIDR prefix (e.g., 24): ")

import ipaddress

print("--- Subnet Calculator ---")

# Get user input
ip_input = input("Enter an IP address (e.g., 192.168.1.1): ")
cidr_input = input("Enter CIDR prefix (e.g., 24): ")

try:
    # Convert CIDR to integer
    cidr = int(cidr_input)

    # Check if CIDR is valid
    if cidr < 0 or cidr > 32:
        print("Error: Invalid IP address or CIDR prefix provided.")
        print(f"Details: '{cidr}' is not a valid netmask")
    else:
        # Try to create a network
        try:
            network = ipaddress.ip_network(ip_input + "/" + str(cidr), strict=False)

            # Calculate usable hosts
            total_hosts = network.num_addresses
            if cidr < 31:
                usable_hosts = total_hosts - 2
            else:
                usable_hosts = 0

            print("Network Address:", network.network_address)
            print("Broadcast Address:", network.broadcast_address)
            print("Number of Usable Hosts:", usable_hosts)

        except ValueError as e:
            print("Error: Invalid IP address or CIDR prefix provided.")
            print("Details:", e)

except ValueError as e:
    print("Error: Invalid IP address or CIDR prefix provided.")
    print("Details:", e)

print("-------------------------")
