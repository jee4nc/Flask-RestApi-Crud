#   Se importa el framework
#   Metodo jsonif y sirve para convertir datos a json
#   request permite poder recibir los datos que se le mandan al servidor
from flask import Flask, jsonify, request

#   Se instancia el framework
app = Flask(__name__)

#   Importo mi archivo de prueba con los datos
from products import products

# Proceso de testeo para ver si funciona o no
@app.route('/ping') #Defino ruta
def ping():  #Metodo que llama la ruta
    return jsonify({"message": "pong!"}) # Lo que hace 

@app.route('/products')
def getProducts():
    return jsonify({"products": products, "message": "Product List"})

#Esta ruta permite poder recibir una propiedad dinamica
#se ocupa entre <> y se especifica el tipo de dato
@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        return jsonify({"product": productFound[0]})
    return jsonify({"message": "Product not found"})

# Se determina el tipo de metodo post o another
@app.route('/products', methods=['POST'])
def addProduct():
   # print(request.json) # request.json permite recibir SOLO los datos en formato json
   new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity'],
        }
   products.append(new_product)
   return jsonify({"message": "Product added succefully", "products": products})

@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
     #Quiero buscar un producto por cada producto en la lista producto y si
     #un producto coincide con producto name
    productFound = [product for product in products if product['name'] == product_name]
    if(len(productFound) > 0 ):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message": "Product Updated",
            "product" : productFound[0]
            })
    return jsonify({"message": "Product Not Found"})

@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    if len(productFound) > 0:
        products.remove(productFound[0])
        return jsonify({
            "message": "Product Deleted",
            "products": products
            })
    return jsonify({"message": "Product Not FOund"})

if __name__ == '__main__':
    app.run(debug=True, port=4000)

