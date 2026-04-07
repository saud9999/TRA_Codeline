import paramiko

hostname = "127.168.100.69"
username = "saud"
key_path = "/Users/saud/Desktop/TRA_Codeline/SSH/id_rsa_paramiko"

# Load private key
key = paramiko.RSAKey.from_private_key_file(key_path)

# Create SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect using SSH key
    client.connect(hostname=hostname, username=username, pkey=key)

    print("Connected successfully using SSH key!")

    # Run a test command
    stdin, stdout, stderr = client.exec_command("uname -a")
    print(stdout.read().decode())

finally:
    client.close()