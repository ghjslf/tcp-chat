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
        else:
            try:
                client.send('message delivery...'.encode('utf_8'))
            except:
                client.close()
                clients.remove(connection)


def successful_delivery_notification_broadcast(connection, clients):
    for client in clients:
        if client != connection:
            try:
                client.send('done!'.encode('utf_8'))
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
                print(f'{address}: {message}')
                if message != '0kDIzkDOKd77':
                    direct = None # TODO парсинг и захват адреса или псевдонима из сообщения прим. @anon
                    if direct:
                        pass # TODO отправка личного сообщения
                    else:
                        logging.info(f'{address}: {message}')
                        broadcast(connection, address, message, clients)
                else:
                    try:
                        # TODO пока адреса или псевдонимы не хранятся с сокетами клиентов получатель оповещает о получении сообщения всех клиентов кроме себя
                        # если в чате 2 клиента то оповещение всех кроме отправителя это нормально
                        successful_delivery_notification_broadcast(connection, clients)
                    except:
                        connection.close()
                        clients.remove(connection)


logging.basicConfig(filename="app.log", level=logging.INFO)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print('2 additional arguments are expected: ip, port')
    exit()

server.bind((str(sys.argv[1]), int(sys.argv[2])))
server.listen(16)

clients = {}

while True:
    connection, address = server.accept()
    clients.append(connection)
    print(f'{address} connected')

    threading.Thread(target=client_processing, args=(connection, address, clients), daemon=True).start()

