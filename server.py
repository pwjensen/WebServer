import errno
import os
import signal
import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 1024


def zombie_killer(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,          # Wait for any child process
                 os.WNOHANG  # Do not block and return EWOULDBLOCK error
            )
        except OSError:
            return

        if pid == 0:  # no more zombies
            return


def handle_request(client_connection):
    request = client_connection.recv(1024).decode()
    # Simple parsing to get the requested URL (naive approach, doesn't handle all cases)
    request_line = request.splitlines()[0]
    requested_file = request_line.split()[1].lstrip('/')

    if requested_file == '':
        requested_file = 'index.html'  # Serve index.html by default

    try:
        # Open and read the requested file
        with open(requested_file, 'rb') as file:
            content = file.read()
            # Determine content type based on the file extension
            if requested_file.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/html'
            # Build the HTTP response
            http_response = f'HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n'.encode() + content
            client_connection.sendall(http_response)
    except FileNotFoundError:
        # Send a 404 Not Found response if the file doesn't exist
        client_connection.sendall(b"HTTP/1.1 404 Not Found\n\n404 Not Found")




def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))

    signal.signal(signal.SIGCHLD, zombie_killer)

    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            # restart 'accept' if it was interrupted
            if code == errno.EINTR:
                continue
            else:
                raise

        pid = os.fork()
        if pid == 0:  # child
            listen_socket.close()  # close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:  # parent
            client_connection.close()  # close parent copy and loop over

if __name__ == '__main__':
    serve_forever()