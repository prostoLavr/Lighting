int pin_array[3] = {13, 12};
void setup() {
  for (int i : pin_array){
    pinMode(i, 1);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0){
    int r = Serial.read() - '0';
    int pin = pin_array[r / 3];
    int mode = r % 3;
    if (mode == 2){
      Serial.print(digitalRead(pin));
    }else{
      digitalWrite(pin, mode);
    }
  }
}
