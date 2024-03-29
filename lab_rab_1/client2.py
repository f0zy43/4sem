import socket
import easygui


def pin(client_socket, numBlinks):
    client_socket.send(numBlinks.encode())
    pin_response = client_socket.recv(1024).decode()
    pin_response2 = client_socket.recv(1024).decode()
    print(f"Вы выбрали {pin_response, pin_response2} пины")


def random_count(client_socket, numBlinks):
    client_socket.send(numBlinks.encode())
    rand_response = client_socket.recv(1024).decode()
    print(f"Генерируем {rand_response} миганий")

    
def count(client_socket, numBlinks):
    client_socket.send(numBlinks.encode())
    count_response = client_socket.recv(1024).decode()
    print(f"Генерируем {count_response} миганий")


def run_client():
    host = 'localhost'
    port = 2892
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    while True:
        choice = easygui.buttonbox("Выберите что-нибудь:", choices=["Выбрать пины", "Пара", "1", "2", "Выйти"])
####################################################################################################################
        if choice == "Выбрать пины":
            client_socket.send("PINS".encode())
            response = client_socket.recv(1024).decode()
            if response == "READY":
                message = easygui.enterbox("Введите номера пинов: ")
                pin(client_socket, message)
####################################################################################################################
        if choice == "Пара":
            choice = easygui.buttonbox("Выберите что-нибудь:", choices=["Рандом", "Свое значение"])
            if choice == "Рандом":
                client_socket.send("PAIR_RANDOM".encode())
                response = client_socket.recv(1024).decode()
                if response == "READY":
                    message = easygui.enterbox("Введите два числа через пробел: ")
                    random_count(client_socket, message)
            if choice == "Свое значение":
                client_socket.send("PAIR_COUNT".encode())
                response = client_socket.recv(1024).decode()
                if response == "READY":
                    message = easygui.enterbox("Введите число: ")
                    count(client_socket, message)
####################################################################################################################
        if choice == "1":
            choice = easygui.buttonbox("Выберите что-нибудь:", choices=["Рандом", "Свое значение"])
            if choice == "Рандом":
                client_socket.send("YEL_RANDOM".encode())
                response = client_socket.recv(1024).decode()
                if response == "READY":
                    message = easygui.enterbox("Введите два числа через пробел: ")
                    random_count(client_socket, message)
            if choice == "Свое значение":
                client_socket.send("YEL_COUNT".encode())
                response = client_socket.recv(1024).decode()
                if response == "READY":
                    message = easygui.enterbox("Введите число: ")
                    count(client_socket, message)
####################################################################################################################
        if choice == "2":
            choice = easygui.buttonbox("Выберите что-нибудь:", choices=["Рандом", "Свое значение"])
            if choice == "Рандом":
                client_socket.send("RED_RANDOM".encode())
                response = client_socket.recv(1024).decode()
                if response == "READY":
                    message = easygui.enterbox("Введите два числа через пробел: ")
                    random_count(client_socket, message)
            if choice == "Свое значение":
                client_socket.send("RED_COUNT".encode())
                response = client_socket.recv(1024).decode()
                if response == "READY":
                    message = easygui.enterbox("Введите число: ")
                    count(client_socket, message)
####################################################################################################################
        elif choice == "Выйти":
            print("Адьес")
            break
    client_socket.close()
if __name__ == '__main__':
    run_client()













