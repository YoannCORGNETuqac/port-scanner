import sys
import socket
import threading

def test_tcp_connection(ip: str, port: int) -> None:
    """
    Test the TCP connection to a given <ip> at a given <port>
    """
    # create TCP socket with IPv4 address
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1) # if the connexion takes more than 1 second, the port is considered closed

    # run connexion
    if not tcpSocket.connect_ex((ip, port)):
        print(f"--> Port {port}/TCP is open.")
    tcpSocket.close()

def scan_range(ip: str, first_port: int, last_port: int):
    """
    Scan a range of ports between <first_port> and <last_port> from a given <ip>
    """
    # create all the threads
    threads = [
        threading.Thread(target=test_tcp_connection, args=(ip, port), daemon=True)
        for port in range(first_port, last_port+1)
    ]

    # start the threads
    [thread.start() for thread in threads if thread is not None]

    # wait for all the threads to be finished
    [thread.join() for thread in threads if thread is not None]

if __name__ == '__main__':
    # verify command arguments
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <target ip or hostname>")
        sys.exit(1)

    # get hostname/IP from command arguments
    target_hostname = sys.argv[1]
    try:
        # get ip from hostname
        target_ip = socket.gethostbyname(target_hostname)
    # Hostname resolution error
    except socket.gaierror:
        print("Hostname could not be resolved: [Errno 11001] getaddrinfo failed.")
        sys.exit(11001)

    print(f"Scanning {target_ip}...")

    try:
        scan_range(target_ip, 0, 1023)
    # Stop program with Ctrl+C
    except KeyboardInterrupt:
        print("Scan is stopping...")

    print("Scan completed successfully.")