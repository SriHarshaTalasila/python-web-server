import socket
import os
import threading

import os

def handle_client(client_socket):
    """Handles a single client request securely."""
    try:
        # Receive request
        request = client_socket.recv(1024).decode("utf-8")
        if not request:
            return

        # Extract HTTP request path
        request_line = request.split("\n")[0]
        method, path, _ = request_line.split()

        # If the request is "/", serve "index.html"
        if path == "/":
            path = "/index.html"

        # Normalize the requested path
        normalized_path = os.path.normpath(path.lstrip("/"))

        # 🔴 Ensure the path does not contain invalid sequences
        if ".." in normalized_path or "~" in normalized_path or normalized_path.startswith("etc") or normalized_path.startswith("C:"):
            print("🚨 [SECURITY ALERT] Directory Traversal Attempt Blocked!")
            response = "HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n<h1>403 Forbidden</h1>"
            client_socket.sendall(response.encode())
            return

        # Construct the secure file path inside the "www" directory
        www_path = os.path.abspath("www")  # Get absolute path of www/
        file_path = os.path.abspath(os.path.join(www_path, normalized_path))

        # 🚨 Ensure the file stays inside "www"
        if not file_path.startswith(www_path + os.sep):
            print(f"🚨 [SECURITY ALERT] Attempted Unauthorized Access: {file_path}")
            response = "HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n<h1>403 Forbidden</h1>"
            client_socket.sendall(response.encode())
            return

        # Serve the file if it exists
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{content}"
        else:
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>"

        client_socket.sendall(response.encode())

    finally:
        client_socket.close()  # Close the connection after response




def start_server():
    host = "127.0.0.1"
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server running on http://{host}:{port}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Start a new thread for each client
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

        except KeyboardInterrupt:
            print("\nServer shutting down...")
            server_socket.close()
            break  # Exit the loop safely

if __name__ == "__main__":
    os.makedirs("www", exist_ok=True)

    if not os.path.exists("www/index.html"):
        with open("www/index.html", "w") as f:
            f.write("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>Secure Web Page</title>
            </head>
            <body>
                <h1>My Secure Web Server</h1>
                <p>Accessing unauthorized files is blocked!</p>
            </body>
            </html>
            """)

    start_server()
