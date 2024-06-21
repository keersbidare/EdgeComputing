from scapy.all import IP,UDP,Raw,send
def sendPacket(ip):
    # Define the destination IP and port
    dest_ip = ip # Replace with the IP address of Device 2
    dest_port = 49153  # Replace with the desired destination port

    # Create the packet
    payload = "Hello from broker, this is a test message to check if the entire payload is sent and received without truncation."
    packet = IP(dst=dest_ip)/UDP(dport=dest_port)/Raw(load=payload)

    # Send the packet
    send(packet)

    print(f"Packet sent to {dest_ip}:{dest_port}")