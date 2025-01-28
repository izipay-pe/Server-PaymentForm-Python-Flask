from flask import Flask, request, redirect, url_for, json, jsonify
from flask_cors import CORS
from key import credentials
import base64
import requests
import json
import hmac
import hashlib
from decimal import Decimal

app = Flask(__name__)
CORS(app)

# Manejo de solicitudes POST para la ruta formtoken
@app.post('/formtoken')
def formulario():
    if not request.get_json(): raise Exception("no post data received!")
    request_data = request.get_json()

    # Obtener el usuario y las claves API
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
        "currency": request_data["currency"],
        "customer": {
            "email": request_data["email"],
            "billingDetails": {
                "firstName": request_data["firstName"],
                "lastName": request_data["lastName"],
                "identityType": request_data["identityType"],
                "identityCode": request_data["identityCode"],
                "phoneNumber": request_data["phoneNumber"],
                "address": request_data["address"],
                "country": request_data["country"],
                "state": request_data["state"],
                "city": request_data["city"],
                "zipCode": request_data["zipCode"]
            }
        },
        "orderId": request_data["orderId"]
    }
    
    # Definir los encabezados de la solicitud
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth,
    }

    # Crear la conexión a la API para la creación del FormToken
    response = requests.post(url, json=data, headers=headers)
    # Obtener la respuesta de la solicitud
    response_data = response.json()

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


# Manejo de solicitudes POST para la ruta validate
@app.post('/validate')
def paidResult():
    if not request.get_json(): raise Exception("no post data received!")
    
    if not checkHash(request.get_json(), credentials["HMACSHA256"]) : raise Exception("Invalid signature")
    
    return jsonify(True), 200 

# Manejo de solicitudes POST para la ruta ipn
@app.post('/ipn')
def ipn():
    if not request.form: raise Exception("no post data received!")

    if not checkHash(request.form, credentials["PASSWORD"]) : raise Exception("Invalid signature")

    # Asignando los valores de la respuesta IPN en las variables
    answer = request.form.get('kr-answer')

    # Convertir el kr-answer en Json
    answer_json = json.loads(answer)

    transaction = answer_json['transactions'][0]
    orderStatus = answer_json['orderStatus']
    orderId = answer_json['orderDetails']['orderId']
    transactionUuid = transaction['uuid']
    
    # Retorna una respuesta HTTP 200
    return 'OK! OrderStatus is ' + orderStatus, 200

def checkHash(reqPost, key):
    answerHash = hmac.new(key.encode('utf-8'), reqPost.get("kr-answer").encode('utf-8'), hashlib.sha256).hexdigest()
    hash = reqPost.get('kr-hash')
    return hash == answerHash


if __name__ == '__main__':
    app.run(debug=True)
