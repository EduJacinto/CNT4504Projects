import socket
import subprocess
import threading


def perform_operation(op):
	result = ''
	if op == 1:
		try:
			result = subprocess.run(['date'], stdout=subprocess.PIPE)
			return result.stdout
		except subprocess.SubprocessError as e:
			result = f'Error: {e}'
			return result.encode()

	elif op == 2:
		try:
			result = subprocess.run(['uptime'], stdout=subprocess.PIPE)
			return result.stdout
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()

	elif op == 3:
		try:
			result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE)
			return result.stdout
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()
	elif op == 4:
		try:
			result = subprocess.run(['netstat', '-tunlp'], stdout=subprocess.PIPE)
			return result.stdout
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()

	elif op == 5:
		try:
			result = subprocess.run(['who'], stdout=subprocess.PIPE)
			return result.stdout
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()
	elif op == 6:
		try:
			result = subprocess.run(['ps', '-ef'], stdout=subprocess.PIPE)
			return result.stdout
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()
	else:
		return "invalid request".encode()
	

def handle_client(client_socket,client_address):
		print(f"connection from:{client_address} ")
		with client_socket:
			while True:
				request =client_socket.recv(1024)
				if not request: 
					print("client disconnected")
					break 

				try:
					op=int(request.decode())
					print(f"Recieved operation request: {op}")
					
					if op==7:
						print("\nshutdown command recieved.")
						client_socket.sendall("server shutting down..".encode())
						client_socket.close()
						return
					
					response=perform_operation(op)
					
				except ValueError:
					response="Invalid request format".encode()
					print("Recieved invalid request format")

				try:
					client_socket.sendall(response)
					print("Response sent to the client")
					


				except BrokenPipeError as bp:
					print(f"Broken Pipe error: Client {client_address} disconnected before response sent")
					break
				except Exception as e:
					print(f"Unexpected error handling client {client_address} {e}")
					break



def spin_up():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(('0.0.0.0', 2998))
		print(f"socket bound to port {2998}")
		s.listen(25)

	while True:
			try:
				client_socket, client_address = s.accept()
				print(f"Connection from:{client_address}")
				
				client_thread= threading.Thread(target=handle_client,args=(client_socket,client_address))
				client_thread.daemon=True
				client_thread.start()
			except KeyboardInterrupt:
				print("\n Servr shutting down")
				break
			except Exception as e:
				print(f"Unexpected error in main server loop: {e}")
 

if __name__ == "__main__":
	spin_up()