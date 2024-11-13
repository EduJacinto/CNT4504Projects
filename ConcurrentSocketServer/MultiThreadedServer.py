import socket
import subprocess


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


def spin_up():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(('0.0.0.0', 2998))
		print(f"socket bound to port {2998}")
		s.listen(25)

		while True:
			client_socket, client_address = s.accept()
			print(f"Connection from:{client_address}")
			
			with client_socket:
				request = client_socket.recv(1024)

				if not request:
					print("Client disconnected")
					continue

				try:
					op = int(request.decode())
					print(f"\nReceived operation request: {op}")
					
					if op == 7:
						s.shutdown(socket.SHUT_RDWR)
						s.close()
						print("\nServer no longer listening. Shutting down...")
						return
					
					response = perform_operation(op)
				except ValueError:
					response = "Invalid request format".encode()
					print("Received invalid request format")

				try:
					client_socket.sendall(response)
					print("\nResponse sent to the client")
				except BrokenPipeError as bp:
					print(f"Broken Pipe Error: Client {client_address} disconnected before response sent")

if __name__ == "__main__":
	spin_up()