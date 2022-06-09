from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        if len(items) == 0:
            return {"item": None}, 404
        for item in items:
            if item['name'] == name:
                return item
            return {'item': None}, 404

    def post(self, name):
        item = {'name': name, 'price': 12.00}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        if len(items) == 0:
            return {"item": None}, 404
        for item in items:
            if item['name'] == name:
                items.remove(item)
                return {'message': 'item removed'}, 204
        return {"item": None}, 404

    def put(self, name):
        data = request.get_json()
        if len(items) == 0:
            item = {'name': name, 'price': 12.00}
            items.append(item)
            return item, 201
        for item in items:
            if item["name"] == name:
                if data["price"] != item["price"]:
                    item["price"] = data["price"]
                    return {"message": "Price updated to " + str(data["price"])}, 204
                else:
                    return {
                        "message": "Price is already at " + str(data["price"])
                    }, 200
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
