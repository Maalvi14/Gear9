import socket
import struct

UDP_IP = "192.168.0.25"  # Replace with your computer's IP address
UDP_PORT = 20777         # Port you've set in the game

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for data on {UDP_IP}:{UDP_PORT}")

def parse_car_telemetry_data(data):
    car_telemetry_data = struct.unpack('<HfffBbhHHHBBBBBB', data[:19])
    telemetry_dict = {
        'throttle': car_telemetry_data[1],
        'brake': car_telemetry_data[3],
    }
    return telemetry_dict

while True:
    data, addr = sock.recvfrom(2048)  # Buffer size is 2048 bytes
    header = struct.unpack('<HBBBBQfHHBBf', data[:28])
    packet_id = header[4]

    if packet_id == 6:  # Car Telemetry Packet
        car_telemetry_data = parse_car_telemetry_data(data[28:28+19*22])
        for i in range(22):
            telemetry_data = car_telemetry_data(data[28 + i*19: 28 + (i+1)*19])
            print(f"Car {i}: Throttle: {telemetry_data['throttle']}, Brake: {telemetry_data['brake']}")

