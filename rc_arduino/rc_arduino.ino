#include <SoftwareSerial.h>

SoftwareSerial RemoteControl(0, 1);  // RX, TX
int command;  // Command from computer through bluetooth

void setup() {
  // bluetooth setup
  RemoteControl.begin(9600);
  RemoteControl.println("Ready for command");
  
  // motor channels setup
  pinMode(12, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);
}

void loop() {
  if (RemoteControl.available()) {
    command = RemoteControl.read();
    if (command == '8') {
      go_forward();
    }
    else if (command == '2') {
      go_backward();
    }
    else if (command == '4') {
      turn_right();
    }
    else if (command == '6') {
      turn_left();
    }
    else {
      brake();
    }
  }
}

void go_forward() {
  // Motor channel A
  digitalWrite(12, HIGH); // forward direction
  digitalWrite(9, LOW);  // disengage brake
  analogWrite(3, 255);  // speed
  
  // Motor channel B
  digitalWrite(13, HIGH);  // forward direction
  digitalWrite(8, LOW);  // disengage brake
  analogWrite(11, 255); // speed
}

void go_backward() {
  // Motor channel A
  digitalWrite(12, LOW); // forward direction
  digitalWrite(9, LOW);  // disengage brake
  analogWrite(3, 255);  // speed
  
  // Motor channel B
  digitalWrite(13, LOW);  // forward direction
  digitalWrite(8, LOW);  // disengage brake
  analogWrite(11, 255); // speed
}

void turn_left() {
  // Motor channel A
  digitalWrite(12, LOW); // backward direction
  digitalWrite(9, LOW);  // disengage brake
  analogWrite(3, 255);  // speed
  
  // Motor channel B
  digitalWrite(13, HIGH);  // forward direction
  digitalWrite(8, LOW);  // disengage brake
  analogWrite(11, 255); // speed
}

void turn_right() {
  // Motor channel A
  digitalWrite(12, HIGH); // forward direction
  digitalWrite(9, LOW);  // disengage brake
  analogWrite(3, 255);  // speed
  
  // Motor channel B
  digitalWrite(13, LOW);  // backward direction
  digitalWrite(8, LOW);  // disengage brake
  analogWrite(11, 255); // speed
}

void brake() {
  digitalWrite(9, HIGH);  // engage brake of channel A
  digitalWrite(8, HIGH);  // engage brake of channel B
}
