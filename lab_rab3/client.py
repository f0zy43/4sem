import socket
import easygui
import matplotlib.pyplot as plt
import pickle


def show_temp(temperature_values, min_temperature, max_temperature, avg_temperature):
    if min_temperature is not None and max_temperature is not None:
        easygui.msgbox(f"Значение: {temperature_values}\nМинимальная температура: {min_temperature}\nМаксимальная температура: {max_temperature}\nСредняя температура: {avg_temperature}\n")
        
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(temperature_values)
        plt.xlabel("Время")
        plt.ylabel("Температура")
        plt.title("График температуры")
        plt.tight_layout()
        plt.show()

def show_hum(humidity_values, min_humidity, max_humidity, avg_humidity):
     if min_humidity is not None and max_humidity is not None:
        easygui.msgbox(f"Минимальная влажность: {min_humidity}\nМаксимальная влажность: {max_humidity}\nСредняя влажность: {avg_humidity}")
            
        plt.subplot(2, 1, 2)
        plt.plot(humidity_values)
        plt.xlabel("Время")
        plt.ylabel("Влажность")
        plt.title("График влажности") 
        plt.tight_layout()
        plt.show()

def show_sound(sound_values, min_sound, max_sound, avg_sound):
     if min_sound is not None and max_sound is not None:
            easygui.msgbox(f"Минимальное значение звука: {min_sound}\nМаксимальное значение звука: {max_sound}\nСреднее значение звука: {avg_sound}")
            
            plt.plot(sound_values)
            plt.xlabel("Время")
            plt.ylabel("Уровень звука")
            plt.title("График уровня звука")
            plt.tight_layout()
            plt.show()



def run_client():
    host = 'localhost'
    port = 2892
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    while True:
        choice = easygui.buttonbox("Выберите что-нибудь:", choices=["Температура", "Влажность", "Звук", "Выйти"])
####################################################################################################################
        if choice == "Температура":
                choice = easygui.buttonbox("Выберите что-нибудь:", choices=["Все время", "Интервал"])
                if choice == "Все время":
                    client_socket.send("TEMP_ALL_TIME".encode())
                    response = client_socket.recv(1024).decode()
                    if response == "READY":
                        data = client_socket.recv(1024)
                        result = pickle.loads(data)
                        temp = result[0]
                        min_temp = result[-3]
                        max_temp = result[-2]
                        avg_temp = result[-1]
                        show_temp(temp, min_temp, max_temp, avg_temp)
                if choice == "Интервал":
                    client_socket.send("TEMP_INT_TIME".encode())
                    start_time = easygui.enterbox("Введите начальное время:")
                    end_time = easygui.enterbox("Введите конечное время:")
                    client_socket.send(start_time.encode())
                    client_socket.send(end_time.encode())
                    response = client_socket.recv(1024).decode()
                    if response == "READY":
                        data = client_socket.recv(1024)
                        result = pickle.loads(data)
                        temp = result[0]
                        min_temp = result[-3]
                        max_temp = result[-2]
                        avg_temp = result[-1]
                        show_temp(temp, min_temp, max_temp, avg_temp)
####################################################################################################################
        if choice == "Влажность":
                choice = easygui.buttonbox("Выберите что-нибудь:", choices=["Все время", "Интервал"])
                if choice == "Все время":
                    client_socket.send("HUM_ALL_TIME".encode())
                    response = client_socket.recv(1024).decode()
                    if response == "READY":
                        data = client_socket.recv(1024)
                        result = pickle.loads(data)
                        hum = result[0]
                        min_hum = result[-3]
                        max_hum = result[-2]
                        avg_hum = result[-1]
                        show_hum(hum, min_hum, max_hum, avg_hum)
                if choice == "Интервал":
                    client_socket.send("HUM_INT_TIME".encode())
                    start_time = easygui.enterbox("Введите начальное время:")
                    end_time = easygui.enterbox("Введите конечное время:")
                    client_socket.send(start_time.encode())
                    client_socket.send(end_time.encode())
                    response = client_socket.recv(1024).decode()
                    if response == "READY":
                        data = client_socket.recv(1024)
                        result = pickle.loads(data)
                        temp = result[0]
                        min_temp = result[-3]
                        max_temp = result[-2]
                        avg_temp = result[-1]
                        show_hum(temp, min_temp, max_temp, avg_temp)
####################################################################################################################
        if choice == "Звук":
                choice = easygui.buttonbox("Выберите что-нибудь:", choices=["Все время", "Интервал"])
                if choice == "Все время":
                    client_socket.send("SOUND_ALL_TIME".encode())
                    response = client_socket.recv(1024).decode()
                    if response == "READY":
                        data = client_socket.recv(1024)
                        result = pickle.loads(data)
                        hum = result[0]
                        min_hum = result[-3]
                        max_hum = result[-2]
                        avg_hum = result[-1]
                        show_sound(hum, min_hum, max_hum, avg_hum)
                if choice == "Интервал":
                    client_socket.send("SOUND_INT_TIME".encode())
                    start_time = easygui.enterbox("Введите начальное время:")
                    end_time = easygui.enterbox("Введите конечное время:")
                    client_socket.send(start_time.encode())
                    client_socket.send(end_time.encode())
                    response = client_socket.recv(1024).decode()
                    if response == "READY":
                        data = client_socket.recv(1024)
                        result = pickle.loads(data)
                        sound = result[0]
                        min_sound = result[-3]
                        max_sound = result[-2]
                        avg_sound = result[-1]
                        show_sound(sound, min_sound, max_sound, avg_sound)
####################################################################################################################
        elif choice == "Выйти":
             break

    client_socket.close()
if __name__ == '__main__':
    run_client()