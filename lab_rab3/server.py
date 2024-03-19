import socket
import serial.tools.list_ports
import serial
import sqlite3
from datetime import datetime
import threading
import pickle


################  определяем порт  #################################
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
arduino = serial.Serial(detect_arduino_port(), baudrate=9600)


###################################################################################
"""подключаем и создаем БД"""
conn = sqlite3.connect('sensor_data.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    timestamp DATETIME,
                    sensor_id TEXT,
                    temperature REAL,
                    humidity REAL,
                    sound_level INTEGER
                 )''')
conn.commit()


###################################################################################
class SensorData:
    def __init__(self, timestamp, sensor_id, temperature, humidity, sound_level):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.humidity = humidity
        self.sound_level = sound_level


class Database:
    def insert_data(timestamp, sensor_id, temperature, humidity, sound_level):
        cursor.execute("INSERT INTO sensor_data (timestamp, sensor_id, temperature, humidity, sound_level) VALUES (?, ?, ?, ?, ?)",
                    (timestamp, sensor_id, temperature, humidity, sound_level))
        conn.commit()

    def fetch_data():
        cursor.execute("SELECT * FROM sensor_data")
        data = cursor.fetchall()
        return [SensorData(*row[0:]) for row in data]


class Func_all_time:

    def temp(data):
        temperature_values = [item.temperature for item in data if item.sensor_id == '1']
        
        if temperature_values:
            min_temperature = min(temperature_values)
            max_temperature = max(temperature_values)
            avg_temperature = sum(temperature_values) / len(temperature_values)
        else:
            min_temperature = max_temperature = avg_temperature = None

        
        return temperature_values, min_temperature, max_temperature, avg_temperature
    
    def humidity(data):
        humidity_values = [item.humidity for item in data if item.sensor_id == '1']
        if humidity_values:
            min_humidity = min(humidity_values)
            max_humidity = max(humidity_values)
            avg_humidity = sum(humidity_values) / len(humidity_values)
        else:
            min_humidity = max_humidity = avg_humidity = None

        return humidity_values, min_humidity, max_humidity, avg_humidity
    
    def sound(data):
        sound_values = [item.sound_level for item in data if item.sensor_id == '2']
        
        min_sound = min(sound_values) if sound_values else None
        max_sound = max(sound_values) if sound_values else None
        avg_sound = sum(sound_values) / len(sound_values)

        return sound_values, min_sound, max_sound, avg_sound


class Func_interval_time:
    def temp_interval(data, start_time, end_time):
        temperature_values = [item.temperature for item in data if item.sensor_id == '1' and start_time <= item.timestamp <= end_time]
        
        if temperature_values:
            min_temperature = min(temperature_values)
            max_temperature = max(temperature_values)
            avg_temperature = sum(temperature_values) / len(temperature_values)
        else:
            min_temperature = max_temperature = avg_temperature = None

        
        return temperature_values, min_temperature, max_temperature, avg_temperature
    
    def humidity_interval(data, start_time, end_time):
        humidity_values = [item.humidity for item in data if item.sensor_id == '1' and start_time <= item.timestamp <= end_time]
        if humidity_values:
            min_humidity = min(humidity_values)
            max_humidity = max(humidity_values)
            avg_humidity = sum(humidity_values) / len(humidity_values)
        else:
            min_humidity = max_humidity = avg_humidity = None

        return humidity_values, min_humidity, max_humidity, avg_humidity
    
    def sound_interval(data, start_time, end_time):
        sound_values = [item.sound_level for item in data if item.sensor_id == '1' and start_time <= item.timestamp <= end_time]
        
        min_sound = min(sound_values) if sound_values else None
        max_sound = max(sound_values) if sound_values else None
        avg_sound = sum(sound_values) / len(sound_values)

        return sound_values, min_sound, max_sound, avg_sound


def server_func(data, client_socket): 
    if data == "TEMP_ALL_TIME":
        client_socket.send("READY".encode())
        sensor_data = Database.fetch_data()
        result = Func_all_time.temp(sensor_data)
        pickled_result = pickle.dumps(result)
        client_socket.send(pickled_result)
    if data == "HUM_ALL_TIME":
        client_socket.send("READY".encode())
        sensor_data = Database.fetch_data()
        result = Func_all_time.humidity(sensor_data)
        pickled_result = pickle.dumps(result)
        client_socket.send(pickled_result)
    if data == "SOUND_ALL_TIME":
        client_socket.send("READY".encode())
        sensor_data = Database.fetch_data()
        result = Func_all_time.sound(sensor_data)
        pickled_result = pickle.dumps(result)
        client_socket.send(pickled_result)

    if data == "TEMP_INT_TIME":
        client_socket.send("READY".encode())
        start_time = client_socket.recv(1024).decode()
        end_time = client_socket.recv(1024).decode()
        sensor_data = Database.fetch_data()
        result = Func_interval_time.temp_interval(sensor_data, start_time, end_time)
        pickled_result = pickle.dumps(result)
        client_socket.send(pickled_result)
    if data == "HUM_INT_TIME":
        client_socket.send("READY".encode())
        sensor_data = Database.fetch_data()
        result = Func_all_time.humidity(sensor_data)
        pickled_result = pickle.dumps(result)
        client_socket.send(pickled_result)
    if data == "SOUND_INT_TIME":
        client_socket.send("READY".encode())
        sensor_data = Database.fetch_data()
        result = Func_all_time.sound(sensor_data)
        pickled_result = pickle.dumps(result)
        client_socket.send(pickled_result)

db_lock = threading.Lock()


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
                
                with db_lock:
                    Database.insert_data(timestamp, sensor_id, temperature, humidity, sound_level)
    except KeyboardInterrupt:
        arduino.close()

arduino_thread = threading.Thread(target=read_data_from_arduino)
arduino_thread.start()


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
            server_func(data, client_socket)       
    client_socket.close()
if __name__ == '__main__':
    run_server()
