import socket
import ssl

def connect_to_server(server_host, serveport, buffer_size, key, filename):
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    with socket.create_connection((server_host, server_port)) as sock:
        with context.wrap_socket(sock, server_hostname=server_host) as ssock:
            try:
                with open(filename, 'rb') as file:
                    file_data = file.read()
                    
                    # Send data
                    ssock.sendall(file_data)
    
                    # Receive response
                    received_data = ssock.recv(buffer_size)
    
                    print("Received from server (first 15 characters):")
                    print(' '.join(f'{x:02X}' for x in received_data[:15]))
    
                    # Simple decryption (XOR with key)
                    decrypted = ''.join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(received_data[:15]))
                    print("Decrypted message (first 15 characters):")
                    print(' '.join(decrypted))
                    
            except FileNotFoundError:
                print("File does not exist.")

def main():
    # Configuration
    servers = [
        {'host': '10.1.', 'port': 5004},
        
    ]
    buffer_size = 3000
    key = "HIDDENKEY"  
    filename = input("Specify file name: ")
    
    for server in servers:
        connect_to_server(server['host'], server['port'], buffer_size, key, filename)

if __name__ == "__main__":
    main()
