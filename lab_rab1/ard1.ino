int ledPin = 9;
int ledPin2 = 10;
int numBlinks = 0;
char mode1 = '0';
char mode1_1 = '0';
char mode2 = '0';
char mode2_2 = '0';

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data.startsWith("Blinks:")) {
      data.remove(0, 7);
      int separatorIndex = data.indexOf(":");
      int separatorIndex1 = data.indexOf("+");
      int separatorIndex1_1 = data.indexOf("-");
      int separatorIndex2 = data.indexOf("*");
      int separatorIndex2_2 = data.indexOf("!");
      numBlinks = data.substring(0, separatorIndex).toInt();
      mode1 = data[separatorIndex1 + 1];
      mode1_1 = data[separatorIndex1_1 + 1];
      mode2 = data[separatorIndex2 + 1];
      mode2_2 = data[separatorIndex2_2 + 1];
      
      for (int i = 0; i < numBlinks; i++) {
        digitalWrite(ledPin, mode1 == '1' ? HIGH : LOW);
        digitalWrite(ledPin2, mode1_1 == '1' ? HIGH : LOW);
        delay(500);
        digitalWrite(ledPin, mode2 == '1' ? HIGH : LOW);
        digitalWrite(ledPin2, mode2_2 == '1' ? HIGH : LOW);
        delay(500);
      }
      digitalWrite(ledPin, LOW);
      digitalWrite(ledPin2, LOW);

    }
  }
}










