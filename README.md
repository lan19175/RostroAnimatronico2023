
# Implementación de una interfaz de uso y control para el rostro animatrónico de la Universidad del Valle de Guatemala

En este trabajo se creó una interfaz gráfica para el rostro animatrónico de la Universidad del Valle de GUatemala en donde se unieron los programas de un Chatbot y la detección de emociones por medio de visión por computadora. También se agrega el control de motores por medio de la GUI conectado por UART utilizando comunicación serial.

## Composición de las carpetas

#### Serial_reception

Se encuentra el archivo .ino con la decodificación del protocolo de comunicación para poder instalarla en el microcontrolador correspondiente

#### templates

En esta carpta se encuentran subcarpetas divididas por pantallas y componentes importantes de la GUI. En su mayoría son archivo .kv con la programación de la estética utilizando la librería de Kivy

#### Trainer.py

Archivo que se utiliza al modificar la base de datos del Chatbot o agregar nuevas categorías

#### main.py

Archivo principal del programa, es el que se debe ejecutar para correr el programa y el que contiene todo el funcionamiento backend de la aplicación

#### requirements.txt

Contiene todas las librerías utilizadas para el funcionamiento de este programa. Es el que se utilizará al momento de la creación del virtual enviroment para su ejecución


## Installation

Abrir Windows power shell como administrador

Ejecutar el siguiente comando

```bash
Get-ExecutionPolicy -List ​
```
Revisar en la lista si CurrenUser aparece como RemoteSigned. En caso contrario ejecutar el siguiente comando
```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser ​
```
Una vez se realizó esto se debe proceder a crear una virtual enviroment con Visual Code abriendo una terminal en la carpeta del programa y corriendo los siguientes códigos
```bash
python -m venv myvenv
```
```bash
myvenv\Scripts\activate
```
```bash
pip install -r requirements.txt
```
Existe un error de compatiblidad entre el archivo de Trainer y la librería numpy por lo que debemos instalar una versión anterior ejecutando el siguiente comand
```bash
pip install numpy==1.23.1
```
Ahora ya podemos ejecutar el archivo haciendo click en el botón de play de VSCode al abrir el archivo de main.py o ejecutando el siguiente comando
```bash
python main.py
```
