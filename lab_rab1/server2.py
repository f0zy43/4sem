import socket
import serial.tools.list_ports
import random
import serial


################  определяем порт  ##############################
def detect_arduino_port():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description
    ]
    if not arduino_ports:
        raise IOError("Ардуино не подключено")
    if len(arduino_ports) > 1:
        print("Найдено несколько плат")
    return arduino_ports[0]


################  подключаем ардуино  ##############################
ard = serial.Serial(detect_arduino_port(), baudrate=9600)


################  создаем рандомное число миганий из интервала  ####
def random_count(numBlinks):
    numBlinks = numBlinks.split()
    a, b = map(int, numBlinks)
    numb = str(random.randint(a, b))
    return numb


################  кол-во миганий которое задаем сами  ##############
def count(message):
    return message


################  работа сервера  ##################################
def run_server():
    host = 'localhost'
    port = 2892
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(detect_arduino_port())
    print("Server is running on {}:{}".format(host, port))
    client_socket, addr = server_socket.accept()
    print("Connected to:", addr)
    
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        else:
###################################################################################
            if data == "PAIR_RANDOM":
                client_socket.send("READY".encode())
                message = client_socket.recv(1024).decode()
                result = random_count(message)
                client_socket.send(result.encode())
                ard.write(f'Blinks:{result}+{1}-{1}*{0}!{0}\n'.encode())
            if data == "PAIR_COUNT":
                client_socket.send("READY".encode())
                message = client_socket.recv(1024).decode()
                result = count(message)
                client_socket.send(result.encode())
                ard.write(f'Blinks:{result}+{1}-{1}*{0}!{0}\n'.encode())
###################################################################################
            if data == "YEL_RANDOM":
                client_socket.send("READY".encode())
                message = client_socket.recv(1024).decode()
                result = random_count(message)
                client_socket.send(result.encode())
                ard.write(f'Blinks:{result}+{0}-{1}*{1}!{0}\n'.encode())
            if data == "YEL_COUNT":
                client_socket.send("READY".encode())
                message = client_socket.recv(1024).decode()
                result = count(message)
                client_socket.send(result.encode())
                ard.write(f'Blinks:{result}+{1}-{0}*{0}!{1}\n'.encode())
###################################################################################
            if data == "RED_RANDOM":
                client_socket.send("READY".encode())
                message = client_socket.recv(1024).decode()
                result = random_count(message)
                client_socket.send(result.encode())
                ard.write(f'Blinks:{result}+{1}-{0}*{0}!{1}\n'.encode())
            if data == "RED_COUNT":
                client_socket.send("READY".encode())
                message = client_socket.recv(1024).decode()
                result = count(message)
                client_socket.send(result.encode())
                ard.write(f'Blinks:{result}+{0}-{1}*{1}!{0}\n'.encode())
###################################################################################        
    client_socket.close()
if __name__ == '__main__':
    run_server()