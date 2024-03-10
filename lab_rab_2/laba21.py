import serial
import sqlite3
from datetime import datetime
import easygui
import matplotlib.pyplot as plt
import threading


arduino = serial.Serial('COM6', 9600)


conn = sqlite3.connect('C:/Users/HP/Desktop/laba2/sensor_data.db', check_same_thread=False)
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    timestamp DATETIME,
                    sensor_id TEXT,
                    temperature REAL,
                    humidity REAL,
                    sound_level INTEGER
                 )''')
conn.commit()


class SensorData:
    def __init__(self, timestamp, sensor_id, temperature, humidity, sound_level):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.humidity = humidity
        self.sound_level = sound_level


def insert_data(timestamp, sensor_id, temperature, humidity, sound_level):
    cursor.execute("INSERT INTO sensor_data (timestamp, sensor_id, temperature, humidity, sound_level) VALUES (?, ?, ?, ?, ?)",
                   (timestamp, sensor_id, temperature, humidity, sound_level))
    conn.commit()


def fetch_data():
    cursor.execute("SELECT * FROM sensor_data")
    data = cursor.fetchall()
    return [SensorData(*row[0:]) for row in data]


def show_gui(data):

    sensor_type = easygui.choicebox("Выберите тип датчика:", choices=["1", "2"])
    
    if sensor_type == "1":

        temperature_values = [item.temperature for item in data if item.sensor_id == '1']
        humidity_values = [item.humidity for item in data if item.sensor_id == '1']
        
        if temperature_values:
            min_temperature = min(temperature_values)
            max_temperature = max(temperature_values)
            avg_temperature = sum(temperature_values) / len(temperature_values)
        else:
            min_temperature = max_temperature = avg_temperature = None
        
        if humidity_values:
            min_humidity = min(humidity_values)
            max_humidity = max(humidity_values)
            avg_humidity = sum(humidity_values) / len(humidity_values)
        else:
            min_humidity = max_humidity = avg_humidity = None

        tme = easygui.choicebox("Выберите тип датчика:", choices=["all", "interval"])

        if tme == "all":
            if min_temperature is not None and min_humidity is not None:
                easygui.msgbox(f"Минимальная температура: {min_temperature}\nМаксимальная температура: {max_temperature}\nСредняя температура: {avg_temperature}\n"
                            f"Минимальная влажность: {min_humidity}\nМаксимальная влажность: {max_humidity}\nСредняя влажность: {avg_humidity}")
            
            plt.figure()
            plt.subplot(2, 1, 1)
            plt.plot(temperature_values)
            plt.xlabel("Время")
            plt.ylabel("Температура")
            plt.title("График температуры")
            
            plt.subplot(2, 1, 2)
            plt.plot(humidity_values)
            plt.xlabel("Время")
            plt.ylabel("Влажность")
            plt.title("График влажности")
            
            plt.tight_layout()
            plt.show()

        if tme == "interval":

            start_time = easygui.enterbox("Введите начальное время:")
            end_time = easygui.enterbox("Введите конечное время:")
            
            filtered_temperature_values = [item.temperature for item in data if item.sensor_id == '1' and start_time <= item.timestamp <= end_time]
            
            plt.figure()
            plt.subplot(2, 1, 1)
            plt.plot(filtered_temperature_values)
            plt.xlabel("Время")
            plt.ylabel("Температура")
            plt.title("График температуры за выбранный интервал времени")
            
            plt.subplot(2, 1, 2)
            plt.plot(humidity_values)
            plt.xlabel("Время")
            plt.ylabel("Влажность")
            plt.title("График влажности")
            
            plt.tight_layout()
            plt.show()

    elif sensor_type == "2":

        sound_values = [item.sound_level for item in data if item.sensor_id == '2']
        
        min_sound = min(sound_values) if sound_values else None
        max_sound = max(sound_values) if sound_values else None
        avg_sound = sum(sound_values) / len(sound_values)

        tme = easygui.choicebox("Выберите тип датчика:", choices=["all", "interval"])

        if tme == "all":

            if min_sound is not None and max_sound is not None:
                easygui.msgbox(f"Минимальное значение звука: {min_sound}\nМаксимальное значение звука: {max_sound}\nСреднее значение звука: {avg_sound}")
            
            plt.plot(sound_values)
            plt.xlabel("Время")
            plt.ylabel("Уровень звука")
            plt.title("График уровня звука")
            plt.show()

        if tme == "interval":

            start_time = easygui.enterbox("Введите начальное время:")
            end_time = easygui.enterbox("Введите конечное время:")
            filtered_temperature_values = [item.temperature for item in data if item.sensor_id == '1' and start_time <= item.timestamp <= end_time]
            
            plt.plot(sound_values)
            plt.xlabel("Время")
            plt.ylabel("Уровень звука")
            plt.title("График уровня звука")
            plt.show()

            
def read_data_from_arduino():
    try:
        while True:
            if arduino.in_waiting > 0:
                data = arduino.readline().decode().strip()
                timestamp = datetime.now()
                data_list = data.split(',')
                sensor_id = data_list[0]
                temperature = data_list[1]
                humidity = data_list[2]
                sound_level = data_list[3]
                
                insert_data(timestamp, sensor_id, temperature, humidity, sound_level)
    except KeyboardInterrupt:
        arduino.close()

arduino_thread = threading.Thread(target=read_data_from_arduino)
arduino_thread.start()

try:
    while True:
        sensor_data = fetch_data()
        show_gui(sensor_data)
except KeyboardInterrupt:
    conn.close()

"""
try:
    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode().strip()
            data_list = data.split(',')
            sensor_id = data_list[0]
            temperature = data_list[1]
            humidity = data_list[2]
            sound_level = data_list[3]
                    
            insert_data(sensor_id, temperature, humidity, sound_level)
                    
            sensor_data = fetch_data()
                    
            show_gui(sensor_data)

except KeyboardInterrupt:
    arduino.close()"""
