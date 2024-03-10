#include <DHT.h>


#define DHTPIN 2     // пин, к которому подключен датчик
#define DHTTYPE DHT11   // тип датчика 
#define DHTledPin 8  // Пин, к которому подключен диод датчика DHT

const int soundSensorPin = A0;  // Пин, к которому подключен датчик звука
const int led = 9;

int sensor_id = 0;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(DHTledPin, OUTPUT); // Устанавливаем пин для диода как выход
  pinMode(led, OUTPUT); 
  pinMode(soundSensorPin, INPUT);
  
}

void loop() {
  
    delay(5000);
  int soundValue = analogRead(soundSensorPin);  // Считываем значение с датчика звука
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (humidity > 0)
  {
    digitalWrite(DHTledPin, HIGH);
    delay(1000);
    digitalWrite(DHTledPin, LOW);
  }

  Serial.print(sensor_id = 1); 
  Serial.print(",");
  Serial.print(temperature); // Отправка температуры
  Serial.print(",");
  Serial.print(humidity); // Отправка влажности
  Serial.print(",");
  Serial.println("None"); // Отправка уровня звука




  if(soundValue > 20){
    digitalWrite(led, HIGH);  // Включаем светодиод при обнаружении звука
    delay(1000);  // Ждем некоторое время
    digitalWrite(led, LOW);  // Выключаем светодиод
  }
  

  Serial.print(sensor_id = 2);
  Serial.print(",");
  Serial.print("None"); // Отправка температуры
  Serial.print(",");
  Serial.print("None"); // Отправка влажности
  Serial.print(",");
  Serial.println(soundValue); // Отправка уровня звука

}

