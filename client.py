import socket
import sys
import xml.etree.ElementTree as ET

def read_query_file(query_filename):
    with open(query_filename, "r") as file:
        return file.read()

def save_response_file(response_data, response_filename):
    with open(response_filename, "w") as file:
        file.write(response_data)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <query_file.xml> <response_file.xml>")
        sys.exit(1)

    query_filename = sys.argv[1]
    response_filename = sys.argv[2]

    try:
        query_data = read_query_file(query_filename)
    except FileNotFoundError:
        print(f"Error: Query file '{query_filename}' not found.")
        sys.exit(1)

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 12345))  
    except ConnectionRefusedError:
        print("Error: Unable to connect to the server. Ensure the server is running.")
        sys.exit(1)

    client.sendall(query_data.encode())
    print(f"Query sent to server: {query_filename}")

    response_data = client.recv(4096).decode()
    print("Response received from server.")

    save_response_file(response_data, response_filename)
    print(f"Response saved to: {response_filename}")

    client.close()

if __name__ == "__main__":
    main()
