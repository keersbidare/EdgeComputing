from scapy.all import sniff, Raw
import publisher
# Define the capture filter
capture_filter = "udp port 49153"  # Replace with the port you expect to receive packets on1
# Function to process each captured packet
def packet_callback(packet):
    if packet.haslayer(Raw):
        payload = packet[Raw].load
        print(f"Packet received:",payload)
    if payload:
        publisher.publish()

# Start sniffing
print("Listening for packets...")
sniff(filter=capture_filter, prn=packet_callback, store=0)

