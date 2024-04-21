import socket
import threading

# Server details
SERVER_HOST = 'localhost'
SERVER_PORT = 8888
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)

def client_task():
    """ Task performed by each client thread. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect(SERVER_ADDRESS)

        # Send a simple HTTP GET request
        http_request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(SERVER_HOST)
        client_socket.sendall(http_request.encode())

        # Receive the response
        response = client_socket.recv(4096)  # Adjust buffer size as needed
        print(response.decode())  # Optionally print the response

def run_clients(num_clients):
    """ Run specified number of client threads to simulate multiple connections. """
    threads = []
    for _ in range(num_clients):
        thread = threading.Thread(target=client_task)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Testing using run_clients with different numbers

run_clients(10)
#run_clients(128)
#run_clients(200)