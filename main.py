import socket
from typing import Tuple
import selectors

interfaces = ["ens33", "ens37"]
selector = selectors.DefaultSelector()
mac_to_sock = dict()
all_socks = list()

MAX_PACKET_SIZE = 65535
BROADCAST_ADDRESS = "ff:ff:ff:ff:ff:ff"

def get_mac_addresses(bytes) -> Tuple[str, str]:
    dest_mac_bytes = bytes[:6]
    src_mac_bytes = bytes[6:12]

    # Format MAC addresses as human-readable strings
    dest_mac = ':'.join(f'{b:02x}' for b in dest_mac_bytes)
    src_mac = ':'.join(f'{b:02x}' for b in src_mac_bytes)
    
    return (src_mac, dest_mac)
            
def create_socket(interface: str) -> socket.socket:
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    sock.bind((interface, 0))
    
    return sock

def initialize_packet_event(interface: str):
    sock = create_socket(interface)
    sock.setblocking(False)
    all_socks.append(sock)
    selector.register(sock, selectors.EVENT_READ, data=None)    

for interface in interfaces:
    initialize_packet_event(interface)

def broadcast():
    print("Mac address is unknown, broadcasting!")
    for sock in all_socks:
        sock.send(packet_bytes)

while True:
    events = selector.select(timeout=None)
    for key, mask in events:
        src_sock = key.fileobj
        packet_bytes = src_sock.recv(MAX_PACKET_SIZE)
        (src_mac, dest_mac) = get_mac_addresses(packet_bytes)
        
        if (dest_mac == BROADCAST_ADDRESS):
            broadcast()
        
        if mac_to_sock.__contains__(src_mac) is False:
            mac_to_sock[src_mac] = src_sock
        
        if mac_to_sock.__contains__(dest_mac):
            dest_sock = mac_to_sock[dest_mac]
            dest_sock.send(packet_bytes)
        else:
            broadcast()
            
        

        
        
    

    