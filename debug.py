import socket

UDP_IP = "192.168.0.25"  # Replace with your computer's IP address
UDP_PORT = 20777         # Port you've set in the game

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for data on {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(2048)  # Buffer size is 2048 bytes
    print(f"Data received from {addr}")
    print(f"Raw data: {data}")
    print("-" * 40)
