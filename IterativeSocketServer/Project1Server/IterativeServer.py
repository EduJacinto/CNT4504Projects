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


HOST = '139.62.210.154'
# PORT = 2998


def perform_operation(op):
	result = ""
	if op == 1:
		try:
			result = subprocess.check_output(["date"], text=True)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()

	elif op == 2:
		try:
			result = subprocess.check_output(["uptime"], text=True)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()

	elif op == 3:
		try:
			result = subprocess.check_output(["free", "-h"], text=True)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()
	elif op == 4:
		try:
			result = subprocess.check_output(["netstat", "-tunlp"], text=True)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()

	elif op == 5:
		try:
			result = subprocess.check_output(["who"], text = True)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()
	elif op == 6:
		try:
			result = subprocess.check_output(["ps", "-ef"], text=True)
			return result.encode()
		except subprocess.SubprocessError as e:
			result = f"Error: {e}"
			return result.encode()
	else:
		return "invalid request".encode()


def spin_server():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, ''))
		print(f"socket bound to {HOST}")
		s.listen(25)
		print(f"server listening to Host:{HOST}")

		while True:
			print("Waiting for connection request")
			client_socket, client_address = s.accept()

			with client_socket:
				print(f"connection from:{client_address}")
				connection_msg = 'Client successfully connected to Server'
				client_socket.send(connection_msg.encode())

				request = client_socket.recv(1024)
				if not request:
					print("Client disconnected")
					continue

				response = perform_operation(request)
				client_socket.sendall(response)


if __name__ == "__main__":
	spin_server()

