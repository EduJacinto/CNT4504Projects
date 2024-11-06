# CLIENT = 139.62.210.154
# this program listen for client requests on the specified network address and port
# when a request is received, the program should determine which operation is being requested and
# perform the requested operation and collect the resulting output , it should then reply to
# the client request with the collected output. It should also perform any necessary clean up activites.
# this program should handle one request at a time and support the following functions:

# Date and Time - return the date and time on the server
# Uptime - return how much run-time has elapsed  since the last server boot-up
# Memory Use - returns the current memory usage on the server
# Netstat - returns the list of network conections on the server
# Current Users - returns the list of users currently on the server
# Running Processes - returns the list of programs currently running on the server
import socket
import subprocess


# HOST = '139.62.210.154'
# PORT = 2998


def perform_operation(op):
	result = ''
	if op == 1:
		try:
			# result = subprocess.check_output(["date"], universal_newlines=True)
			result = subprocess.run(['date'], stdout=subprocess.PIPE)
			return result.stdout
		except subprocess.SubprocessError as e:
			result = f'Error: {e}'
			return result.encode()

	elif op == 2:
		try:
			result = subprocess.run(['uptime'], stdout=subprocess.PIPE)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()

	elif op == 3:
		try:
			result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()
	elif op == 4:
		try:
			result = subprocess.run(['netstat', '-tunlp'], stdout=subprocess.PIPE)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()

	elif op == 5:
		try:
			result = subprocess.run(['who'], stdout=subprocess.PIPE)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()
	elif op == 6:
		try:
			result = subprocess.run(['ps', '-ef'], stdout=subprocess.PIPE)
			return result.encode()
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
		# host_address = socket.gethostbyname(socket.gethostname())

		while True:
			client_socket, client_address = s.accept()
			print(f"Connection from:{client_address}")
			
			with client_socket:
				# connection_msg = 'Client successfully connected to Server'
				# client_socket.sendall(connection_msg.encode())
				request = client_socket.recv(1024)
				# print(f"Received request {request.decode()}")

				if not request:
					print("Client disconnected")
					continue

				try:
					op = int(request.decode())
					print(f"Received operation request: {op}")
					response = perform_operation(op)
				except ValueError:
					response = "Invalid request format".encode()
					print("Received invalid request format")

				try:
					client_socket.sendall(response)
					print("Response sent to the client")
				except BrokenPipeError as bp:
					print(f"Broken Pipe Error: Client {client_address} disconnected before response sent")

if __name__ == "__main__":
	spin_up()

