# HOST = 139.62.210.155
# this program should transmit requests to the server on a specified network port, and spawn multiple client sessions
# when spun up, this program should request the network address and port to connect to
# it should ask the user which operation to request from the server, and how many clients (1, 5, 15, 20, 25) to generate
# collect the following data:
# Turn-around Time - elapsed time for each client request
# Total turn-around time - the sum of the turn-around times for all of the client requests
# Average turn-around time - total turn-around time divided by number of client requests
# for testing purposes
import socket
import threading
import time

HOST = '139.62.210.155'


def client_session(port, request, client_id, results):
    try:
        # create the socket for each client
        s = socket.socket()
        s.connect((HOST, port))
        print(f"Connected to server at host {HOST} and port {port}")
        # clock the time when this is session is started
        start_time = time.time()
        # send request to the server
        s.send(request.encode())

        # receive the response from the server
        response = s.recv(1024)
        end_time = time.time()
        print("client received response from server")
        turnaround_time = end_time - start_time
        results.append(turnaround_time)

    except socket.gaierror as e:
        print(f"Client {client_id} encountered Error: {e}")
    finally:
        s.close()


def client_request():
    port = input("Specify which port to connect to: ")
    # s = socket.socket()
    # s.connect((HOST, port))
    # print("Connected to Host: {HOST} via Port:{port}")
    # print(s.recv(1024))

    # continue collecting requests while true
    request = 1
    while True:
        # continue prompting for request while request is invalid
        while True:
            try:
                print("Enter number of request you want to send:\n1) Date and Time\n2) Uptime\n3) Current Memory Usage")
                print("4) List Network Connections\n5) List current Users Connected\n6) List Running Processes\n7) Quit")
                request = int(input())

                if request in (1, 2, 3, 4, 5, 6, 7):
                    break
            except ValueError:
                print("Invalid request")
        # if request is 7 finish program
        if request == 7:
            print("Program exiting...")
            return

        # continue prompting for number of clients to spawn while number is invalid
        while True:
            try:
                client_numbers = int(input("How many clients would you like to spawn:\n1,5, 10, 15, 20, or 25\n"))
                # if valid num clients break out of the loop and continue
                if client_numbers in (1, 5, 10, 15, 20, 25):
                    break
            except ValueError:
                print("Invalid number of clients")
        # END COLLECTING REQUEST PARAMETERS
        # thread will collect thread objects and results will collect the turn around time of each thread
        threads = []
        results = []

        # create a new thread for each client
        for i in range(client_numbers):
            # this is where each thread is sent to the above function and thus to the server
            thread = threading.Thread(target=client_session, args=(port, request, i+1, results))
            threads.append(thread)
            thread.start()
        # make the program wait for all the threads to finish
        for thread in threads:
            thread.join()

        # print turn around time and other turnaround time stats
        print("Printing turn around time for each client:")
        for result in results:
            print(result)

        total_turnaround_time = sum(results)
        avg_turnaround_time = total_turnaround_time / client_numbers
        print(f"Total turnaround time for {client_numbers} clients is: {total_turnaround_time:.2f} seconds")
        print(f"Average turnaround time is: {avg_turnaround_time:.2f} seconds")


if __name__ == "__main__":
    client_request()