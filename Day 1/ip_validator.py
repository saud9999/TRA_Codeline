# Ask the user to enter an IP address
ip = input("Enter an IPv4 address (4 octs): ")

# Split the IP using dots "."
parts = ip.split(".")

# Check if it has exactly 4 parts
if len(parts) != 4:                     # jumps to invalid counts 
    print("Invalid IPv4 address")
else:
    valid = True

    # Check each part
    for part in parts:
        # Must be digits only
        if part.isdigit() == False:
            valid = False
            break

        number = int(part)

        # Must be between 0 and 255
        if number < 0 or number > 255:
            valid = False
            break

    # Final result
    if valid:
        print("Valid IPv4 address")
    else:
        print("Invalid IPv4 address")

print("Enter IP addresses (press Enter on empty line to finish):")

valid_count = 0
invalid_count = 0

while True:
    ip = input("IP: ")

    # Stop if blank line
    if ip == "":
        break

    parts = ip.split(".")

    if len(parts) != 4:
        print("Invalid")
        invalid_count += 1
        continue

    valid = True

    for part in parts:
        if part.isdigit() == False:
            valid = False
            break

        number = int(part)

        if number < 0 or number > 255:
            valid = False
            break

    if valid:
        print("Valid")
        valid_count += 1
    else:
        print("Invalid")
        invalid_count += 1

# Summary
print("\nSummary:")
print(f"Valid IPs:", valid_count)
print(f"Invalid IPs:", invalid_count)