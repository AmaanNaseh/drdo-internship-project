#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver srituhobby = Adafruit_PWMServoDriver();

#define servo1 0
#define servo2 1
#define servo3 2
#define servo4 3

#define ledPin 13  // LED connected to pin 13

void setup() {
  Serial.begin(9600);
  srituhobby.begin();
  srituhobby.setPWMFreq(60);

  pinMode(ledPin, OUTPUT);

  // Home Position
  srituhobby.setPWM(servo1, 0, 330);
  srituhobby.setPWM(servo2, 0, 150);
  srituhobby.setPWM(servo3, 0, 300);
  srituhobby.setPWM(servo4, 0, 410);
  delay(3000);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'P') {
      blinkLED(3);         // Blink LED 3 times
      pickAndPlace();      // Then do pick-and-place
    }
  }
}

void blinkLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(ledPin, HIGH);
    delay(300);
    digitalWrite(ledPin, LOW);
    delay(300);
  }
}

void pickAndPlace() {
  for (int S1value = 330; S1value >= 250; S1value--) {
    srituhobby.setPWM(servo1, 0, S1value);
    delay(10);
  }

  for (int S2value = 150; S2value <= 380; S2value++) {
    srituhobby.setPWM(servo2, 0, S2value);
    delay(10);
  }

  for (int S3value = 300; S3value <= 380; S3value++) {
    srituhobby.setPWM(servo3, 0, S3value);
    delay(10);
  }

  for (int S4value = 410; S4value <= 510; S4value++) {
    srituhobby.setPWM(servo4, 0, S4value);
    delay(10);
  }

  delay(2000);

  for (int S4value = 510; S4value > 410; S4value--) {
    srituhobby.setPWM(servo4, 0, S4value);
    delay(10);
  }

  for (int S3value = 380; S3value > 300; S3value--) {
    srituhobby.setPWM(servo3, 0, S3value);
    delay(10);
  }

  for (int S2value = 380; S2value > 150; S2value--) {
    srituhobby.setPWM(servo2, 0, S2value);
    delay(10);
  }

  for (int S1value = 250; S1value < 450; S1value++) {
    srituhobby.setPWM(servo1, 0, S1value);
    delay(10);
  }

  for (int S2value = 150; S2value <= 380; S2value++) {
    srituhobby.setPWM(servo2, 0, S2value);
    delay(10);
  }

  for (int S3value = 300; S3value <= 380; S3value++) {
    srituhobby.setPWM(servo3, 0, S3value);
    delay(10);
  }

  for (int S4value = 410; S4value <= 510; S4value++) {
    srituhobby.setPWM(servo4, 0, S4value);
    delay(10);
  }

  for (int S4value = 510; S4value > 410; S4value--) {
    srituhobby.setPWM(servo4, 0, S4value);
    delay(10);
  }

  for (int S3value = 380; S3value > 300; S3value--) {
    srituhobby.setPWM(servo3, 0, S3value);
    delay(10);
  }

  for (int S2value = 380; S2value > 150; S2value--) {
    srituhobby.setPWM(servo2, 0, S2value);
    delay(10);
  }

  for (int S1value = 450; S1value > 330; S1value--) {
    srituhobby.setPWM(servo1, 0, S1value);
    delay(10);
  }
}
