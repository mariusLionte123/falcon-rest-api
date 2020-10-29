import falcon, json
from uuid import uuid4

from db import Database

database = Database("db.txt")

class ObjRequestClass:
    __json_input = {}
    def __validate_json_input(self, req: falcon.Request):
        try:
            self.__json_input = json.loads(req.stream.read())
        except ValueError:
            self.__json_input = {}

    def on_get(self, req: falcon.request.Request, res: falcon.Response, product_id=None):
        res.status = falcon.HTTP_200

        if product_id is None:
            result = database.get()
            res.media = result
            return

        
        result = database.get(product_id)
        if len(result) == 0:
            res.status = falcon.HTTP_404
            res.body = json.dumps({"message":"Product not Found", "error": True})
            return
        else:
            product, = result
            res.media = product
                
            

    def on_post(self, req:falcon.Request, res: falcon.Response):
        self.__validate_json_input(req)

        print(self.__json_input)
        self.__json_input.__setitem__("id", str(uuid4()))
        response = database.insert(self.__json_input)

        res.status = falcon.HTTP_201
        res.media=response

    def on_put(self, req:falcon.Request, res: falcon.Response, product_id=None):
        if product_id is None:
            response = {"error": True, "message": "You must provice a valid id"}
            res.media = response
            return

        self.__validate_json_input(req)

        self.__json_input["id"] = product_id
        
        updated_user = database.update(self.__json_input)

        res.status=falcon.HTTP_200
        res.media = updated_user

    def on_delete(self, req: falcon.Request, res: falcon.Response, product_id=None):
        if product_id is None:
            response = {"error": True, "message": "You must provice a valid id"}
            res.media = response
            return

        database.delete(product_id)

        res.status = falcon.HTTP_200
        res.media = {"message": "Product deleted"}

api = falcon.API()
api.add_route('/v1/products', ObjRequestClass())
api.add_route('/v1/products/{product_id}', ObjRequestClass())
