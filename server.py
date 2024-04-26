import socket
import sqlite3
import datetime


SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 1024
DATABASE_FILE = 'data.sqlite3'

def create_table_if_not_exists():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS station_status (
            station_id INT,
            last_date TEXT,
            alarm1 INT,
            alarm2 INT,
            PRIMARY KEY(station_id)
        )'''
        cursor.execute(create_table_query)

        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")

    finally:
        if conn:
            conn.close()

def process_client_data(client_data):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        station_id, alarm1, alarm2 = map(int, client_data.split())

        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        select_query = 'SELECT * FROM station_status WHERE station_id = ?'
        cursor.execute(select_query, (station_id,))
        existing_station = cursor.fetchone()

        if existing_station:
            update_query = '''UPDATE station_status 
                              SET last_date = ?, alarm1 = ?, alarm2 = ? 
                              WHERE station_id = ?'''
            cursor.execute(update_query, (current_datetime, alarm1, alarm2, station_id))
        else:
            insert_query = '''INSERT INTO station_status 
                              (station_id, last_date, alarm1, alarm2) 
                              VALUES (?, ?, ?, ?)'''
            cursor.execute(insert_query, (station_id, current_datetime, alarm1, alarm2))

        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")

    finally:
        if conn:
            conn.close()

def run_server():
    create_table_if_not_exists()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen(5)

    print(f"Server listening on {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Received connection from {client_address[0]}:{client_address[1]}")

        try:
            client_data = client_socket.recv(1024).decode().strip()

            if client_data:
                print(f"Received data from client: {client_data}")
                process_client_data(client_data)

        except socket.error as e:
            print(f"Socket error occurred: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            client_socket.close()

if __name__ == '__main__':
    run_server()
