#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Spring 2023
# Homework 3: Simple web client to interact with proxy
#
# Example usage:
#
#   python3 web_client.py <proxy_host> <proxy_port> <requested_url>

# Python modules
import binascii
import socket
import sys

class WebClient:

    def __init__(self, proxy_host, proxy_port, url):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.url = url
        self.start()

    def start(self):

        # Open connection to proxy
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.connect((self.proxy_host, self.proxy_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)
        
        

        # TODOs
        # Send requested URL to proxy
        
        # parse URL into GET request

        # check if has http at start
        if self.url[:7]=="http://":
            self.url = self.url[7:]

        # split url into host and path
        spl = self.url.split('/')
        urlhost = spl[0]
        urlpath = '/' + '/'.join(spl[1:])

        # prepare request
        req = ("GET " + urlpath + " HTTP/1.1\r\nHost: " 
            + urlhost + "\r\nConnection: close \r\n\r\n")

        print("req: " + req)
        proxy_sock.sendall(req.encode('utf-8'))

        # Receive binary data from proxy
        
        response = self.receive_all(proxy_sock).decode('utf-8')
        print(response)

        

        proxy_sock.close()
    
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
    url = 'http://example.com/'
    #url = 'http://eu.httpbin.org'
    #url = 'http://info.cern.ch/'
    #url = 'http://www-db.deis.unibo.it/'

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])
        url = sys.argv[3]

    web_client = WebClient(proxy_host, proxy_port, url)

if __name__ == '__main__':
    main()
