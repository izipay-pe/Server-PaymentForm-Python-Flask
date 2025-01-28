<p align="center">
  <img src="https://github.com/izipay-pe/Imagenes/blob/main/logos_izipay/logo-izipay-banner-1140x100.png?raw=true" alt="Formulario" width=100%/>
</p>

# Server-PaymentForm-Python-Flask

## Índice

➡️ [1. Introducción](#-1-introducci%C3%B3n)  
🔑 [2. Requisitos previos](#-2-requisitos-previos)  
🚀 [3. Ejecutar ejemplo](#-3-ejecutar-ejemplo)  
🔗 [4. APIs](#4-APIs)  
💻 [4.1. FormToken](#41-formtoken)  
💳 [4.2. Validación de firma](#42-validaci%C3%B3n-de-firma)  
📡 [4.3. IPN](#43-ipn)  
📮 [5. Probar desde POSTMAN](#-5-probar-desde-postman)  
📚 [6. Consideraciones](#-6-consideraciones)

## ➡️ 1. Introducción

En este manual podrás encontrar una guía paso a paso para configurar un servidor API REST (Backend) en **[FLASK]** para la pasarela de pagos de IZIPAY. **El actual proyecto no incluye una interfaz de usuario (Frontend)** y debe integrarse con un proyecto de Front. Te proporcionaremos instrucciones detalladas y credenciales de prueba para la instalación y configuración del proyecto, permitiéndote trabajar y experimentar de manera segura en tu propio entorno local.
Este manual está diseñado para ayudarte a comprender el flujo de la integración de la pasarela para ayudarte a aprovechar al máximo tu proyecto y facilitar tu experiencia de desarrollo.

<p align="center">
  <img src="https://i.postimg.cc/KYpyqYPn/imagen-2025-01-28-082121144.png" alt="Formulario"/>
</p>

## 🔑 2. Requisitos Previos

- Comprender el flujo de comunicación de la pasarela. [Información Aquí](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/start.html)
- Extraer credenciales del Back Office Vendedor. [Guía Aquí](https://github.com/izipay-pe/obtener-credenciales-de-conexion)
- Para este proyecto utilizamos Python 3.12
- Para este proyecto utilizamos la herramienta Visual Studio Code.
  
> [!NOTE]
> Tener en cuenta que, para que el desarrollo de tu proyecto, eres libre de emplear tus herramientas preferidas.

## 🚀 3. Ejecutar ejemplo

### Instalar Plugin "Python"
Python, extensión para Visual Studio Code que ofrece soporte completo para el lenguaje Python (para todas las versiones del lenguaje >= 3.7). Para instalarlo:
1. Ingresar a la sección "Extensiones" de Visual Studio Code
2. Buscar "Python"
3. Instalar extensión

<p align="center">
  <img src="https://i.postimg.cc/XYZKRcNJ/Plugin.png" alt="Plugin" width="850"/>
</p>

### Clonar el proyecto
```sh
git clone https://github.com/izipay-pe/Server-PaymentForm-Python-Flask.git
``` 

### Datos de conexión 

Reemplace **[CHANGE_ME]** con sus credenciales de `API REST` extraídas desde el Back Office Vendedor, revisar [Requisitos previos](#-2-requisitos-previos).

- Editar el archivo `key.py` en la ruta raíz:
```python
credentials = {
    # Identificador de su tienda
    "USERNAME": "~ CHANGE_ME_USER_ID ~",

    # Clave de Test o Producción
    "PASSWORD": "~ CHANGE_ME_PASSWORD ~",

    # Clave Pública de Test o Producción
    "PUBLIC_KEY": "~ CHANGE_ME_PUBLIC_KEY ~",

    # Clave HMAC-SHA-256 de Test o Producción
    "HMACSHA256": "~ CHANGE_ME_HMAC_SHA_256 ~"
}
```

### Preparar el entorno:
Antes de ejecutar el proyecto, se creará el virtual environment (venv):
1. Presionar `ctrl` + `shift` + `p` para abrir la paleta de comandos y buscar `Python: Select Interpreter`
<p align="center">
  <img src="https://i.postimg.cc/yYpXprHt/Select-Interpreter.png" alt="PanelComandos" width="600"/>
</p>
2. Seleccionar `Create Virtual Environment`
<p align="center">
  <img src="https://i.postimg.cc/43fcJ6sV/Create-Env.png" alt="CreateVenv" width="600"/>
</p>
3. Seleccionar el tipo de venv
<p align="center">
  <img src="https://i.postimg.cc/PJ2zjS8L/Venv.png" alt="SelectVenv" width="600"/>
</p>
4. Seleccionar la versión de Python
<p align="center">
  <img src="https://i.postimg.cc/1RHKw3Y9/Select-Python.png" alt="SelectPython" width="600"/>
</p>
5. Seleccionar archivo de dependencias `requirements.txt`
<p align="center">
  <img src="https://i.postimg.cc/pr2Y4wyb/Requirements.png" alt="SelectRequirements" width="600"/>
</p>

### Ejecutar proyecto
1. Para ejecutar el proyecto a través de Visual Studio, ingresar a la sección "Ejecutar" y seleccionar `Run and Debug`
<p align="center">
  <img src="https://i.postimg.cc/8sQdxm4D/Ejecutar.png" alt="SelectInterpreter" width="400"/>
</p>
2. Seleccionar el debugger: `Python Debugger`
<p align="center">
  <img src="https://i.postimg.cc/yxSXfbFv/Debugger.png" alt="SelectRequirements" width="600"/>
</p>
3. Seleccionar la configuración del debugger `Flask`
<p align="center">
  <img src="https://i.postimg.cc/wvrQQps1/Debug-conf.png" alt="SelectRequirements" width="600"/>
</p>
4. El proyecto se ha ejecutado y es accesible a través de:

 ```sh
  http://127.0.0.1:5000
 ```

## 🔗4. APIs
- 💻 **FormToken:** Generación de formToken y envío de la llave publicKey necesarios para desplegar la pasarela.
- 💳  **Validacion de firma:** Se encarga de verificar la autenticidad de los datos.
- 📩 ️ **IPN:** Comunicación de servidor a servidor. Envío de los datos del pago al servidor.

## 💻4.1. FormToken
Para configurar la pasarela se necesita generar un formtoken. Se realizará una solicitud API REST a la api de creación de pagos:  `https://api.micuentaweb.pe/api-payment/V4/Charge/CreatePayment` con los datos de la compra para generar el formtoken. El servidor devuelve el formToken generado junto a la llave `publicKey` necesaria para desplegar la pasarela

Podrás encontrarlo en el archivo `app.py`.

```python
@app.post('/formtoken')
def formulario():
    username = credentials["USERNAME"]
    password = credentials["PASSWORD"]
    publicKey = credentials['PUBLIC_KEY']
    
    # Definir la URL del endpoint
    url = 'https://api.micuentaweb.pe/api-payment/V4/Charge/CreatePayment'
    # Definir la autenticación para la API
    auth = 'Basic ' + base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
   
    # Definir el body de la solicitud
    data = {
        "amount": int(Decimal(request_data["amount"]) * 100),
        ...
        ...
        "orderId": request_data["orderId"]
    }
    
    # Definir los encabezados de la solicitud
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth,
    }
    ...
    ...
    # Ingresa a la condicional si la repuesta es válida
    if response_data['status'] == 'SUCCESS':
        # Extraer el FormToken
        formToken = response_data['answer']['formToken']
        return_data = {
            "formToken": formToken,
            "publicKey": publicKey
        }
        # Envía el formToken y el publicKey
        return jsonify({"formToken": formToken, "publicKey": publicKey}), 200
    else:
        return 'ERROR AL GENERAR FORMTOKEN', 500
```
Podrás acceder a esta API a través:
```bash
localhost:5000/formToken
```
ℹ️ Para más información: [Formtoken](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/embedded/formToken.html)

## 💳4.2. Validación de firma
Se configura la función `checkHash` que realizará la validación de los datos recibidos por el servidor luego de realizar el pago mediante el parámetro `kr-answer` utilizando una clave de encriptación definida en `key`. Podrás encontrarlo en el archivo `app.py`.

```python
def checkHash(reqPost, key):
    answerHash = hmac.new(key.encode('utf-8'), reqPost.get("kr-answer").encode('utf-8'), hashlib.sha256).hexdigest()
    hash = reqPost.get('kr-hash')
    return hash == answerHash
```

Se valida que la firma recibida es correcta. Para la validación de los datos recibidos a través de la pasarela de pagos (front) se utiliza la clave `HMACSHA256`.

```python
@app.post('/validate')
def paidResult():
    if not request.get_json(): raise Exception("no post data received!")
    
    if not checkHash(request.get_json(), credentials["HMACSHA256"]) : raise Exception("Invalid signature")
    
    return jsonify(True), 200 
```
El servidor devuelve un valor booleano `true` verificando si los datos de la transacción coinciden con la firma recibida. Se confirma que los datos son enviados desde el servidor de Izipay.

Podrás acceder a esta API a través:
```bash
localhost:5000/validate
```

ℹ️ Para más información: [Analizar resultado del pago](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/kb/payment_done.html)

## 📩4.3. IPN
La IPN es una notificación de servidor a servidor (servidor de Izipay hacia el servidor del comercio) que facilita información en tiempo real y de manera automática cuando se produce un evento, por ejemplo, al registrar una transacción.

Se realiza la verificación de la firma utilizando la función `checkHash`. Para la validación de los datos recibidos a través de la IPN (back) se utiliza la clave `PASSWORD`. Se devuelve al servidor de izipay un mensaje confirmando el estado del pago.

Se recomienda verificar el parámetro `orderStatus` para determinar si su valor es `PAID` o `UNPAID`. De esta manera verificar si el pago se ha realizado con éxito.

Podrás encontrarlo en el archivo `app.py`.

```python
@app.post('/ipn')
def ipn():
    if not request.form: raise Exception("no post data received!")

    if not checkHash(request.form, credentials["PASSWORD"]) : raise Exception("Invalid signature")
    ...
    ...
    orderStatus = answer_json['orderStatus']
    ...
    ...
    return 'OK! OrderStatus is ' + orderStatus, 200
```
Podrás acceder a esta API a través:
```bash
localhost:5000/ipn
```

La ruta o enlace de la IPN debe ir configurada en el Backoffice Vendedor, en `Configuración -> Reglas de notificación -> URL de notificación al final del pago`

<p align="center">
  <img src="https://i.postimg.cc/XNGt9tyt/ipn.png" alt="Formulario" width=80%/>
</p>

ℹ️ Para más información: [Analizar IPN](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/api/kb/ipn_usage.html)

## 📡4.3.Pase a producción

Reemplace **[CHANGE_ME]** con sus credenciales de PRODUCCIÓN de `API REST` extraídas desde el Back Office Vendedor, revisar [Requisitos Previos](#-2-requisitos-previos).

- Editar el archivo `key.py` en la ruta raíz:
```python
credentials = {
    # Identificador de su tienda
    "USERNAME": "~ CHANGE_ME_USER_ID ~",

    # Clave de Test o Producción
    "PASSWORD": "~ CHANGE_ME_PASSWORD ~",

    # Clave Pública de Test o Producción
    "PUBLIC_KEY": "~ CHANGE_ME_PUBLIC_KEY ~",

    # Clave HMAC-SHA-256 de Test o Producción
    "HMACSHA256": "~ CHANGE_ME_HMAC_SHA_256 ~"
}
```

## 📮 5. Probar desde POSTMAN
* Puedes probar la generación del formToken desde POSTMAN. Coloca la URL con el metodo POST con la ruta `/formToken`.
  
```bash
localhost:5000/formToken
```

* Datos a enviar en formato JSON raw:
 ```node
{
    "amount": 1000,
    "currency": "PEN", //USD
    "orderId": "ORDER12345",
    "email": "cliente@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "phoneNumber": "123456789",
    "identityType": "DNI",
    "identityCode": "ABC123456",
    "address": "Calle principal 123",
    "country": "PE",
    "city": "Lima",
    "state": "Lima",
    "zipCode": "10001"
}
```

## 📚 6. Consideraciones

Para obtener más información, echa un vistazo a:

- [Formulario incrustado: prueba rápida](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/quick_start_js.html)
- [Primeros pasos: pago simple](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/javascript/guide/start.html)
- [Servicios web - referencia de la API REST](https://secure.micuentaweb.pe/doc/es-PE/rest/V4.0/api/reference.html)
