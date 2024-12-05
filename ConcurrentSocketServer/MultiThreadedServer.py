import socket
import subprocess
import threading

active_threads = []


def perform_operation(op):
    
    if op == 1:
        try:
            result = subprocess.run(['date'], stdout=subprocess.PIPE)
            return result.stdout  
        except subprocess.SubprocessError as e:
            return f"Error: {e}".encode()  

    elif op == 2:
        try:
            result = subprocess.run(['uptime'], stdout=subprocess.PIPE)
            return result.stdout
        except subprocess.SubprocessError as e:
            return f"Error: {e}".encode()

    elif op == 3:
        try:
            result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE)
            return result.stdout
        except subprocess.SubprocessError as e:
            return f"Error: {e}".encode()

    elif op == 4:
        try:
            result = subprocess.run(['netstat', '-tunlp'], stdout=subprocess.PIPE)
            return result.stdout
        except subprocess.SubprocessError as e:
            return f"Error: {e}".encode()

    elif op == 5:
        try:
            result = subprocess.run(['who'], stdout=subprocess.PIPE)
            return result.stdout
        except subprocess.SubprocessError as e:
            return f"Error: {e}".encode()

    elif op == 6:
        try:
            result = subprocess.run(['ps', '-ef'], stdout=subprocess.PIPE)
            return result.stdout
        except subprocess.SubprocessError as e:
            return f"Error: {e}".encode()

    else:
        return b"invalid request"  


def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")
    with client_socket:  
        while True:
            # I BELIEVE THIS IS THE CODE THAT IS PRODUCING THE ERROR EITHER LINE 63 OR LINE 74
            try:
                
                request = client_socket.recv(1024).decode().strip()
                if not request:
                    print(f"Client {client_address} disconnected.")
                    break

                print(f"Request received from {client_address}: {request}")
                
              
                if request.isdigit():
                    op = int(request)
                    if op == 7: 
                        client_socket.sendall("Server is shutting down.".encode())
                        print("Shutdown command received.")
                        return
                    response = perform_operation(op)
                else:
                    response = "Invalid request format. Please send a valid operation number."

               
                client_socket.sendall(response.encode())
                print(f"Response sent to {client_address}")

            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                break
    print(f"Cleaning up connection with {client_address}")



def spin_up():
    global active_threads
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', 2200))
        print("Socket bound to port 2200")
        server_socket.listen(25)

        try:
            while True:
                try:
                    client_socket, client_address = server_socket.accept()
                    print(f"Accepted connection from {client_address}")

                   
                    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                    active_threads.append(client_thread)  
                    client_thread.start()

                except KeyboardInterrupt:
                    print("\nServer shutting down")
                    break
                except Exception as e:
                    print(f"Unexpected error in main server loop: {e}")

        finally:
            
            print("Waiting for threads to complete...")
            for thread in active_threads:
                thread.join()
            print("All threads have completed.")

if __name__ == "__main__":
    spin_up()
