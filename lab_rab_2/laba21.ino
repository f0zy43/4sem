#include <DHT.h>


#define DHTPIN 2
#define DHTTYPE DHT11 
#define DHTledPin 8

const int soundSensorPin = A0;
const int led = 9;

int sensor_id = 0;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(DHTledPin, OUTPUT);
  pinMode(led, OUTPUT); 
  pinMode(soundSensorPin, INPUT);
  
}

void loop() {
  
    delay(5000);
  int soundValue = analogRead(soundSensorPin);
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
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println("None");




  if(soundValue > 20){
    digitalWrite(led, HIGH);
    delay(1000);
    digitalWrite(led, LOW);
  }
  

  Serial.print(sensor_id = 2);
  Serial.print(",");
  Serial.print("None");
  Serial.print(",");
  Serial.print("None");
  Serial.print(",");
  Serial.println(soundValue);

}

