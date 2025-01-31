// Pin del LED conectado a pin digital 13 (por ejemplo)
const int ledPin = 2; 

void setup() {
  Serial.begin(9600);      // Inicia la comunicación serial
  pinMode(ledPin, OUTPUT);  // Configura el pin del LED como salida
}

void loop() {
  if (Serial.available() > 0) {
    // Lee toda la línea recibida como una cadena de texto
    String input = Serial.readStringUntil('\n');  // Espera hasta recibir un salto de línea
    Serial.print("Valor recibido: ");
    Serial.println(input);
    // Intenta convertir la entrada a un número entero
    int receivedValue = input.toInt();

    // Verifica si la entrada era un número válido
    if (input == String(receivedValue)) {
      

      // Verifica si el valor está en el rango deseado
      if (receivedValue >= 4000 && receivedValue <= 5000) {
        //Serial.println("Valor dentro del rango. Encendiendo LED.");
        digitalWrite(ledPin, HIGH);  // Enciende el LED
        // wdelay(2100)
      } else {
        //Serial.println("Valor fuera del rango. Apagando LED.");
        digitalWrite(ledPin, LOW);   // Apaga el LED
      }
    } else {
      // La entrada no era un número válido
      //Serial.println("Error: Entrada no válida.");
      digitalWrite(ledPin, LOW);  // Asegura que el LED se apague
    }
  } else {
      // La entrada no era un número válido
      // Serial.println("Error: Serial port not available.");
      // digitalWrite(ledPin, LOW);  // Asegura que el LED se apague
    }
}
