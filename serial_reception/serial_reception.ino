#include <Servo.h>

// Define el pin al que está conectado el servo
int servoPin1 = 9;
int servoPin2 = 10;
int servoPin3 = 11;
int servoPin4 = 5;

int servoGrados1 = 100;
int servoGrados2 = 80;
int servoGrados3 = 10;
int servoGrados4 = 33;
int numServos = 19;
String servoVals[19]={"100","80","10","33","25","72","63","54","46","38","177","36","55","140","89","25","30","100","170",};

bool modoManual = false;

char inbyte = 0;
String inbyteString;
String protocoloCase;
String  payload;
char motorNameSeparator = ':';

// Crea un objeto de tipo Servo
Servo miServo;
Servo miServo2;
Servo miServo3;
Servo miServo4;

void setup() {
  // Inicializa el objeto Servo
  miServo.attach(servoPin1);
  miServo2.attach(servoPin2);
  miServo3.attach(servoPin3);
  miServo4.attach(servoPin4);
  Serial.begin(115200);
}

void loop() {
   if (Serial.available()){
    inbyte = Serial.read();
    inbyteString = String(inbyte);
    if (inbyteString == "<"){
      payload = Serial.readStringUntil( '>' );
      protocoloCase = String(payload.charAt(0));
      if (protocoloCase == "#"){
        int separatorIndex = 0;
        separatorIndex = payload.indexOf(motorNameSeparator);
        String motorName = payload.substring(1, separatorIndex);
        if(motorName == "M1"){
          String valorMotor = payload.substring(separatorIndex+1, payload.length());
          servoGrados1 = valorMotor.toInt();
        }else if (motorName == "M2"){
          String valorMotor = payload.substring(separatorIndex+1, payload.length());
          servoGrados2 = valorMotor.toInt();
        }else if (motorName == "M3"){
          String valorMotor = payload.substring(separatorIndex+1, payload.length());
          servoGrados3 = valorMotor.toInt();
        }else{
          String valorMotor = payload.substring(separatorIndex+1, payload.length());
          servoGrados4 = valorMotor.toInt();
        }
      }else if(protocoloCase == "*"){
        modoManual = !modoManual;
      }else if(protocoloCase == "&"){
         servoVals[0] = String(servoGrados1);
         servoVals[1] = String(servoGrados2);
         servoVals[2] = String(servoGrados3);
         servoVals[3] = String(servoGrados4);
         String envio = "<&";
         for (int i=0;i<numServos;i++){
          envio+= servoVals[i];
          envio+= ",";
         }
         envio.remove(envio.length()-1);
         envio+=">";
         Serial.println(envio);
      }else{
        Serial.println("no existe el caso");
      }
    }
  }
  // Mueve el servo a la posición inicial (0 grados)
  miServo.write(servoGrados1);
  miServo2.write(servoGrados2);
  miServo3.write(servoGrados3);
  miServo4.write(servoGrados4);
  delay(10);
}
