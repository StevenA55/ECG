int TiempoMuestreo = 25/9;       // tiempo de muestreo Se encuentra en milisegundos
unsigned long pasado = 0;     // tiempo pasado (Se hace para asegurar tiempo de muestreo)
unsigned long ahora;
void setup() {
  Serial.begin(9600);
  pinMode(10, INPUT);
  pinMode(11, INPUT);

}

void loop() {
  ahora = millis();
  int CambioTiempo = ahora - pasado;
  if (CambioTiempo >= TiempoMuestreo)
  {
    if ((digitalRead(10) == 1) || (digitalRead(11) == 1)) {
      Serial.println('!');
    }
    else {
      Serial.println(analogRead(A0));
    }
  }
}
