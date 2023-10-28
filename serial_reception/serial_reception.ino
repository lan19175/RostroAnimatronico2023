/*******************************************************************************
* Copyright (c) 2016, ROBOTIS CO., LTD.
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*
* * Redistributions of source code must retain the above copyright notice, this
*   list of conditions and the following disclaimer.
*
* * Redistributions in binary form must reproduce the above copyright notice,
*   this list of conditions and the following disclaimer in the documentation
*   and/or other materials provided with the distribution.
*
* * Neither the name of ROBOTIS nor the names of its
*   contributors may be used to endorse or promote products derived from
*   this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
* FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
* DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
* SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
* OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*******************************************************************************/
#include <ArduinoJson.h>
/*
 * Serial_HelloWorld
*/
String x;
char inbyte = 0;
int bandera_escuchando = 0;
int bandera_select_variable = 0;
char  inst_servo1[7];
char  inst_servo19[133];
int index_inst_servo1 = 0;
int imprimir = 0;
String  payload;
String intent;
int response;
int resultado;
DynamicJsonDocument doc(2048);
DeserializationError error;

void setup() {
  Serial.begin(9600);
}

void loop() {
 if (Serial.available()){
    inbyte = Serial.read();
    x = String(inbyte);
  }
 if (x == "<"){
     bandera_escuchando = 1;
     index_inst_servo1 = 0;
     bandera_select_variable = 0;
     memset(inst_servo1, 0, sizeof(inst_servo1));
     memset(inst_servo19, 0, sizeof(inst_servo19));
  }
  
  while (bandera_escuchando == 1){
    if (Serial.available()){
      inbyte = Serial.read();
      x = String(inbyte);
      if (x == ">"){
        bandera_escuchando = 0;
        bandera_select_variable = 0;
        imprimir = 1;
      }else if(x == "<"){
        imprimir = 0;
        resultado = 0;
      }else if (x == "#"){
        bandera_select_variable = 1;
        resultado = 1;
      }else if (x == "&"){
        bandera_select_variable = 2;
        resultado = 2;
      }else if (x == "%"){
        resultado = 3;
        if (bandera_select_variable == 3){
          bandera_select_variable = 4;
          resultado = 4;
        }
        bandera_select_variable = 3;
      }else{
        if (bandera_select_variable == 1){
          inst_servo1[index_inst_servo1] = inbyte;
        }else if (bandera_select_variable == 2){
          inst_servo19[index_inst_servo1] = inbyte;
        }else if (bandera_select_variable == 3){
          payload = Serial.readStringUntil( '\n' );
          error = deserializeJson(doc, payload);
        }else if (bandera_select_variable == 4){
          response = x.toInt();
          intent = Serial.readStringUntil( '\n' );
        }
        index_inst_servo1++;
      }
    }
  }
  if (imprimir == 1){
    if (resultado == 1){
      Serial.print(inst_servo1);
      Serial.print("*");
    }else if (resultado == 2){
      Serial.println(inst_servo19);
      Serial.print("*");
    }else if (resultado == 3){
      if (error){
        Serial.println("hubo error*");
      }else{
        if(doc["Despedida"][0] == "Bye"){
          Serial.print("recibido responses*");
        }else{
          Serial.print("no se recibio bien el mensaje*");
        }
        
      }
    }else if (resultado == 4){
      const char* hablando = doc["Despedida"][0];
      Serial.print(hablando);
      Serial.print("###");
      Serial.print(response);
      Serial.print("*");
    }
    imprimir = 0;
  } 
}
