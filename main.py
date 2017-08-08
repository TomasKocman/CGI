#!python3

from http.server import HTTPServer, CGIHTTPRequestHandler


def main():
	server = ("localhost", 8080)
	serverObject = HTTPServer(server, CGIHTTPRequestHandler)
	serverObject.serve_forever()


if  __name__ == '__main__':
	main()
