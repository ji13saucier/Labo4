from Server import Lab4HTTPRequestHandler
from socketserver import TCPServer


if __name__ == '__main__':
    with TCPServer(('', 8080), Lab4HTTPRequestHandler) as tcp_server:
        print('Serving on http://localhost:8080')
        tcp_server.serve_forever()

