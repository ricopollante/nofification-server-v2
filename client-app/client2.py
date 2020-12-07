import socket

def TCPrcv():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 5080))
    while True:
        data = sock.recv(1024)
        #print(len(data))
        if len(data.decode('UTF')) == 0:
            continue
            sock.close()
        else:
            print(data)
            sock.close()
            TCPrcv()

TCPrcv()