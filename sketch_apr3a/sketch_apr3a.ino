int pin_array[3] = {13, 12};
void setup() {
  for (int i : pin_array){
    pinMode(i, 1);
    digitalWrite(i, HIGH);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0){
    int r = Serial.read() - '0';
    int pin = pin_array[r / 3];
    int mode = r % 3;
    if (mode == 2){
      Serial.print( !bool(digitalRead(pin)) );
    }else{
      digitalWrite(pin, !bool(mode));
    }
  }
}
