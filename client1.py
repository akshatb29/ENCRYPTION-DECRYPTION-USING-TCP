import socket
import ssl
import requests

def connect_to_server(server_host, server_port, buffer_size, key, filename, ca_cert):
    # Create a socket
    context = ssl.create_default_context(cafile=ca_cert)

    try:
        with socket.create_connection((server_host, server_port)) as sock:
            with context.wrap_socket(sock, server_hostname='encrypto') as ssock:
                while True:
                    # Send data
                    ssock.sendall(filename.encode('utf-8'))

                    # Receive response
                    received_data = ssock.recv(buffer_size)

                    if received_data:
                        print("Received from server:")
                        print(' '.join(f'{x:02X}' for x in received_data))

                        # Simple decryption (XOR with key)
                        decrypted = ''.join(chr(text ^ ord(key[7 % len(key)])) for text in list(received_data))
                        print("Decrypted message:")
                        print(' '.join(decrypted))
                        break
    except Exception as e:
        print("error: ",e)
        print("File not found on the server.")

def main():
    # Configuration
    servers = [
        {'host': '192.168.155.81', 'port': 5004},
    ]
    buffer_size = 3000
    key = "HIDDENKEY"  # This should match the length requirement based on your actual use case

    filename = input("Specify file name: ")
    ca_cert = "server.crt"  # Path to your CA certificate file

    for server in servers:	
        connect_to_server(server['host'], server['port'], buffer_size, key, filename, ca_cert)

if __name__ == "__main__":
    main()
