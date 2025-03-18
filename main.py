import socket
import struct

interfaces = ["ens33", "ens37"]

# def is_packet_from_me(packet):
#     for interface in interfaces:    
#         print(f"packet mac: {packet[scapy.all.Ether].src}, interface mac: {packet[scapy.all.Ether].src}")
#         if scapy.all.Ether in packet and packet[scapy.all.Ether].src == scapy.all.get_if_hwaddr(interface):
#             return True
#     return False

# def send_packet_safe(packet, interface):
#     print(packet.summary())
#     packet[scapy.all.Ether].src = scapy.all.get_if_hwaddr(interface)
#     scapy.all.sendp(packet, iface=interface)

# def process_packet(packet):
#     for interface in interfaces:
#         if (packet.sniffed_on.__contains__(interface) is False and is_packet_from_me(packet) is False):
#             send_packet_safe(packet, interface)
            
def create_socket(interface) -> socket.socket:
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    sock.bind((interface, 0))
    
    return sock

def get_mac_addresses(bytes):
    eth_header = bytes[:14]
    dest_mac, src_mac, ethertype = struct.unpack('!6s6sH', eth_header)

    # Format MAC addresses as human-readable strings
    dest_mac = ':'.join(f'{b:02x}' for b in dest_mac)
    src_mac = ':'.join(f'{b:02x}' for b in src_mac)
    
    return (src_mac, dest_mac)

MAX_PACKET_SIZE = 65535
    
first = create_socket("ens33")
second = create_socket("ens37")    

while True:
    bytes = first.recv(MAX_PACKET_SIZE)
    (src_mac, dest_mac) = get_mac_addresses(bytes)
    print(f"source: {src_mac}, dest: {dest_mac}")
    
    if (dest_mac == "ff:ff:ff:ff:ff:ff" or dest_mac == "00:0c:29:76:82:fd"):
        print("received packet intended for second interface, sending it.")
        second.sendall(bytes)
        print("waiting for response")
        response = second.recv(MAX_PACKET_SIZE)
        print("response recevied!")
        (res_src_mac, res_dest_mac) = get_mac_addresses(response)
        
        if (res_dest_mac == "00:0c:29:b1:3d:04"):
            first.sendall(response)
        
        
    

    