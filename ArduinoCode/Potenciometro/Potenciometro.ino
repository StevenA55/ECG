#define graph A0
float lectura, signal1;
float voltaje1;
int coma1,n, led;
String datos, numero, indice;

unsigned long tiempo1, tiempo2;
unsigned long t1 = 0, t2 = 1;

void setup() {
  Serial.begin(9600);
  pinMode(graph, INPUT);
}

void loop() {
  tiempo1 = millis();
  tiempo2 = millis();

  signal1 = analogRead(A0);
  voltaje1 = ((signal1/1023)*5.5);
  if (tiempo1-t1>=200){
    t1= tiempo1;
    Serial.println(voltaje1);
  }

}
