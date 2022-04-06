import socket
import sys
import threading
import logging


def broadcast(connection, address, message, clients):
    for client in clients:
        if client != connection:
            try:
                client.send(f'{address}: {message}'.encode('utf_8'))
            except:
                client.close()
                clients.remove(connection)


def client_processing(connection, address, clients):
    connection.send('welcome'.encode('utf-8'))

    while True:
        try:
            message = connection.recv(2048).decode('utf_8')
        except:
            continue
        else:
            if not message:
                if connection in clients:
                    clients.remove(connection)
            else:
                direct = None
                if direct:
                    pass
                else:
                    logging.info(f'{address}: {message}')
                    print(f'{address}: {message}')
                    broadcast(connection, address, message, clients)


logging.basicConfig(filename="app.log", level=logging.INFO)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print('2 additional arguments are expected: ip, port')
    exit()

server.bind((str(sys.argv[1]), int(sys.argv[2])))
server.listen(16)

clients = []

while True:
    connection, address = server.accept()
    clients.append(connection)
    print(f'{address} connected')

    threading.Thread(target=client_processing, args=(connection, address, clients), daemon=True).start()

