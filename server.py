import socket
import pandas as pd
import xml.etree.ElementTree as ET

def parse_query(query):
    conditions = []
    root = ET.fromstring(query)
    for condition in root.findall("condition"):
        column = condition.find("column").text.strip()
        value = condition.find("value").text.strip()
        conditions.append((column, value))
    return conditions

def validate_conditions(df, conditions):
    valid_columns = set(df.columns)
    for column, _ in conditions:
        if column not in valid_columns:
            return False
    return True

def filter_data(df, conditions):
    filtered_df = df
    for column, value in conditions:
        filtered_df = filtered_df[filtered_df[column] == value]
    return filtered_df

def create_response(status, data=None):
    root = ET.Element("result")
    status_elem = ET.SubElement(root, "status")
    status_elem.text = status

    if status == "success" and data is not None:
        data_elem = ET.SubElement(root, "data")
        for _, row in data.iterrows():
            row_elem = ET.SubElement(data_elem, "row")
            ET.SubElement(row_elem, "name").text = row["Name"]
            ET.SubElement(row_elem, "title").text = row["Title"]
            ET.SubElement(row_elem, "email").text = row["Email"]

    return ET.tostring(root, encoding="unicode")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Server is running and listening for connections...")

    df = pd.read_csv("directory.csv") 

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection received from {client_address}")

        query_data = client_socket.recv(4096).decode()
        print(f"Received query: {query_data}")

        try:
            conditions = parse_query(query_data)
            if not validate_conditions(df, conditions):
                response = create_response("fail")
            else:
                filtered_data = filter_data(df, conditions)
                response = create_response("success", filtered_data)

        except Exception as e:
            print(f"Error processing query: {e}")
            response = create_response("fail")

        client_socket.sendall(response.encode())

        client_socket.close()
        print("Response sent, connection closed.")

if __name__ == "__main__":
    main()
