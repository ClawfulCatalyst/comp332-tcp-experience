#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Spring 2023
# Homework 3: Simple multi-threaded web proxy

# Usage:
#   python3 web_proxy.py <proxy_host> <proxy_port> <requested_url>
#

# Python modules
import socket
import sys
import threading


class WebProxy():

    def __init__(self, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_backlog = 1
        self.web_cache = {}
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.bind((self.proxy_host, self.proxy_port))
            proxy_sock.listen(self.proxy_backlog)

        except OSError as e:
            print ("Unable to open proxy socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        # Wait for client connection
        while True:
            client_conn, client_addr = proxy_sock.accept()
            print ('Client with address has connected', client_addr)
            thread = threading.Thread(
                    target = self.serve_content, args = (client_conn, client_addr))
            thread.start()

    def serve_content(self, client_conn, client_addr):

        # Todos
        # Receive request from client
        request = (self.receive_all(client_conn)).decode('utf-8')
        print(request)

        # parse host
        spl = request.split('\r\n')
        host = (spl[1])[6:]
        print("host: " + host)

        # Send request to web server
        try:
            host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_sock.connect((host,80))
            print("Connected to Host")
        except OSError as e:
            print("Unable to connect to host: ", e)
            if host_sock:
                host_sock.close()
            sys.exit(1)

        host_sock.sendall(request.encode('utf-8'))
        
        # Wait for response from web server
        response = self.receive_all(host_sock).decode('utf-8')
        print(response)
        
        # Send web server response to client
        client_conn.sendall(response.encode('utf-8'))


        # Close connection to client
        client_conn.close()

    def receive_all(self, client_conn):
        buff = b""
        while True:
            try:
                cur = client_conn.recv(1024)
                buff += cur
                if len(cur) < 1024: break
            except TimeoutError:
                break
        return buff
                
            

def main():

    print (sys.argv, len(sys.argv))

    proxy_host = 'localhost'
    proxy_port = 50008

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])

    web_proxy = WebProxy(proxy_host, proxy_port)

if __name__ == '__main__':

    main()
