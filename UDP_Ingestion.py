import socket
import struct

UDP_IP = "192.168.0.25"  # Replace with your computer's IP address
UDP_PORT = 20777         # Port you've set in the game

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for data on {UDP_IP}:{UDP_PORT}")

# Define the packet header struct format according to F1 23 UDP specification
packet_header_format = '<HBBBBQfIIB'
packet_header_size = struct.calcsize(packet_header_format)

while True:
    try:
        data, addr = sock.recvfrom(2048)  # Buffer size is 2048 bytes
        print(f"Data received from {addr}")

        # Check the length of the received data
        print(f"Received data length: {len(data)}")

        if len(data) >= packet_header_size:
            # Print the raw header data
            raw_header = data[:packet_header_size]
            print(f"Raw header data: {raw_header}")

            # Extracting and printing the header for debugging
            try:
                header = struct.unpack(packet_header_format, raw_header)
                print(f"Unpacked header: {header}")

                packet_format, game_year, game_major_version, game_minor_version, packet_version, session_uid, session_time, frame_identifier, player_car_index, secondary_player_car_index = header
                print(f"Packet Format: {packet_format}, Game Year: {game_year}, Game Version: {game_major_version}.{game_minor_version}, Packet Version: {packet_version}")
                print(f"Session UID: {session_uid}, Session Time: {session_time}, Frame Identifier: {frame_identifier}, Player Car Index: {player_car_index}, Secondary Player Car Index: {secondary_player_car_index}")

                # Debug individual bytes for session_uid and session_time
                session_uid_bytes = struct.unpack('<Q', raw_header[6:14])
                session_time_bytes = struct.unpack('<f', raw_header[14:18])
                frame_identifier_bytes = struct.unpack('<I', raw_header[18:22])
                player_car_index_byte = struct.unpack('<B', raw_header[22:23])
                secondary_player_car_index_byte = struct.unpack('<B', raw_header[23:24])
                
                print(f"Session UID Bytes: {session_uid_bytes}, Session Time Bytes: {session_time_bytes}")
                print(f"Frame Identifier Bytes: {frame_identifier_bytes}, Player Car Index Byte: {player_car_index_byte}, Secondary Player Car Index Byte: {secondary_player_car_index_byte}")

            except struct.error as e:
                print(f"Unpacking error: {e}")

            packet_id = packet_version  # Assuming packet_version indicates the packet ID for telemetry packets
            print(f"Packet ID: {packet_id}")

            if packet_id == 6:  # Car Telemetry Packet
                car_telemetry_data = data[packet_header_size:]
                start = player_car_index * 60  # Each Car Telemetry Data block is 60 bytes
                end = start + 60
                if len(car_telemetry_data[start:end]) == 60:
                    telemetry_data = struct.unpack('<HfffBbhHHHBBBBBB', car_telemetry_data[start:end])
                    print(f"Player Car Throttle: {telemetry_data[1]}, Brake: {telemetry_data[3]}")
                else:
                    print(f"Incomplete car telemetry data for player car index {player_car_index}")
        else:
            print("Received packet is too short to contain a valid header")
    except Exception as e:
        print(f"Error: {e}")
