int laserPin = 10;  // Connect laser module to pin 10

void setup() {
    pinMode(laserPin, OUTPUT);  
    digitalWrite(laserPin, HIGH);  // Turn laser ON
}

void loop() {
    // Do nothing, keeps running infinitely with laser ON
}
