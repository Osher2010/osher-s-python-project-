import time
import socket

SERVER_ADDRESS = '127.0.0.1'  
SERVER_PORT = 1024
STATUS_FILE = 'status.txt'
WAIT_SECONDS = 3

def read_file():
    with open(STATUS_FILE, 'r') as file:
        station_id = int(file.readline().strip())
        alarm1_state = int(file.readline().strip())
        alarm2_state = int(file.readline().strip())
    return station_id, alarm1_state, alarm2_state

def send_to_server(station_id, alarm1_state, alarm2_state):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    
    data = f'{station_id} {alarm1_state} {alarm2_state}'
    client_socket.sendall(data.encode())

    
    client_socket.close()

def run_client():
    while True:
        station_id, alarm1_state, alarm2_state = read_status_file()
        send_data_to_server(station_id, alarm1_state, alarm2_state)
        print("Data sent successfully to the server.")

        time.sleep(WAIT_SECONDS)
