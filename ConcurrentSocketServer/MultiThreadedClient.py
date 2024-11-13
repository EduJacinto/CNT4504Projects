import socket
import threading
import time

def client_session(host, port, request, client_id, results):
    try:
        # create the socket for each client
        s = socket.socket()
        s.settimeout(5)
        s.connect((host, port))
        # clock the time when this is session is started
        start_time = time.time()
        # send request to the server
        s.sendall(str(request).encode())

        try:
            # receive the response from the server
            response = s.recv(4096).decode()
            end_time = time.time()
            if response:
                print(f"\nclient {client_id} received response from server:\n{response}")
            else:
                print(f"\nClient{client_id} did not recieve a response from the server.")

            turnaround_time = end_time - start_time
            results.append(turnaround_time)

        except socket.timeout:
            print(f"\nClient {client_id} timed out waiting for server")

    except socket.gaierror as e:
        print(f"\nClient {client_id} encountered Error: {e}")

    finally:
        s.close()


def client_request():
    host = input("Enter host IP: ")
    port = int( input("Specify which port to connect to: ") )

    # continue collecting requests while true
    while True:
        # continue prompting for request while request is invalid
        while True:
            try:
                print("Enter number of request you want to send:\n1) Date and Time\n2) Uptime\n3) Current Memory Usage")
                print("4) List Network Connections\n5) List current Users Connected\n6) List Running Processes\n7) Quit")
                request = int(input())

                if request in (1, 2, 3, 4, 5, 6, 7):
                    break
            except ValueError: # if not in set of acceptable values, catch the error and recover, print error message
                print("Invalid request")
        # if request is 7 close program
        if request == 7:
            print("\nShutting down server...")
            try:
                s = socket.socket()
                s.connect((host, port))
                s.sendall(str(request).encode())
            except socket.timeout:
                print("\nTimeout error")
            finally:
                s.close()
            print("\nProgram exiting...")
            return

        # continue prompting for number of clients to spawn while number is invalid
        while True:
            try:
                client_numbers = int(input("\nHow many clients would you like to spawn:\n1, 5, 10, 15, 20, or 25\n"))
                # if valid num clients break out of the loop and continue
                if client_numbers in (1, 5, 10, 15, 20, 25):
                    break
            except ValueError: # catch and recover if request not in set of acceptable values
                print("\nInvalid number of clients")
        # END COLLECTING REQUEST PARAMETERS
        # thread will collect thread objects and results will collect the turn around time of each thread
        threads = []
        results = []

        # create a new thread for each client
        for i in range(client_numbers):
            # this is where each thread is sent to the above function and thus to the server
            thread = threading.Thread(target=client_session, args=(host, port, request, i+1, results))
            threads.append(thread)
            thread.start()
        # make the program wait for all the threads to finish
        for thread in threads:
            thread.join()

        # print turn around time and other turnaround time stats
        print("\nPrinting turn around time for each client:")
        for result in results:
            print(result)

        total_turnaround_time = sum(results)
        avg_turnaround_time = total_turnaround_time / client_numbers
        print(f"\nTotal turnaround time for {client_numbers} clients is: {total_turnaround_time:.2f} seconds")
        print(f"\nAverage turnaround time for {client_numbers} clients is: {avg_turnaround_time:.2f} seconds\n")


if __name__ == "__main__":
    client_request()