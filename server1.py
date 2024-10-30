import socket
import ssl
import threading

def handle_client(conn, addr, key):
    buffer_size = 3000
    print("Connection from:", addr)

    try:
        while True:
            
            data = conn.recv(buffer_size)
            if not data:
                break  
            
           
            xor_data = bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(data)])
            
            
            with open("temp.txt", "w") as file:
                for byte in xor_data:
                    file.write(f'{byte:X}')
            
            
            conn.sendall(xor_data)
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def start_server(host, port, key, certfile, keyfile):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on:", host, port)
    
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    
    while True:
        conn, addr = server_socket.accept()
        conn_ssl = context.wrap_socket(conn, server_side=True)
        thread = threading.Thread(target=handle_client, args=(conn_ssl, addr, key))
        thread.start()
        print("Active connections:", threading.activeCount() - 1)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5004
    KEY = "HIDDENKEY"
    CERTFILE = "server.crt"
    KEYFILE = "server.key"
    
    start_server(HOST, PORT, KEY, CERTFILE, KEYFILE)
