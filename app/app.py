import falcon, json

from db import Database

database = Database([{
        "id":"1",
        "name": "Product 1",
        "description": "Product 1 Description",
        "price": 1234}])

class ObjRequestClass:
    __json_input = {}
    def __validate_json_input(self, req: falcon.Request):
        try:
            self.__json_input = json.loads(req.stream.read())
            return True
        except ValueError:
            self.__json_input = {}
            return False

    def on_get(self, req: falcon.request.Request, res: falcon.Response):
        input_is_valid = self.__validate_json_input(req)

        res.status = falcon.HTTP_200

        if input_is_valid and "id" in self.__json_input:
            result = database.get(self.__json_input["id"])
            if len(result) == 0:
                res.status = falcon.HTTP_404
                res.body = json.dumps({"message":"Product not Found", "error": True})
                return
            else:
                product, = result
                res.media = product
                return
        else:
            result = database.get()
            res.media = result

    def on_post(self, req:falcon.Request, res: falcon.Response):
        input_is_valid = self.__validate_json_input(req)

        if input_is_valid == False:
            res.status = falcon.HTTP_422
            response = {
                "message": "invalid input",
                "error": True
            }
            res.media=response

        res.status = falcon.HTTP_201
        
        response = database.insert(self.__json_input)

        res.media=response

    def on_put(self, req:falcon.Request, res: falcon.Response):
        input_is_valid = self.__validate_json_input(req)

        res.status = falcon.HTTP_422
        if input_is_valid == False:
            response = {"error": True, "message": "Invalid input format"}
            res.media = response
            return

        if "id" not in self.__json_input:
            response = {"error": True, "message": "You must provice a valid id"}
            res.media = response
            return

        user_id = self.__json_input["id"]

        user_found = database.get(user_id)

        if len(user_found) == 0:
            response = {"error": True, "message": "Invalid id value"}
            res.media = response
            return
        
        user, = user_found
        for key in self.__json_input:
            user[key] = self.__json_input[key]
        
        updated_user = database.update(user)

        res.status=falcon.HTTP_200
        res.media = updated_user

    def on_delete(self, req: falcon.Request, res: falcon.Response):
        input_is_valid = self.__validate_json_input(req)

        res.status = falcon.HTTP_422
        if input_is_valid == False:
            response = {"error": True, "message": "Invalid input format"}
            res.media = response
            return

        if "id" not in self.__json_input:
            response = {"error": True, "message": "You must provice a valid id"}
            res.media = response
            return

        database.delete(self.__json_input["id"])

        res.status = falcon.HTTP_200
        res.media = {"message": "Product deleted"}

api = falcon.API()
api.add_route('/api', ObjRequestClass())
