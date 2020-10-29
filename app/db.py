import json

class Database:
    def __init__(self, file="", data=[]):
        self.file = file
        db = self.read_file()

        if db.read() == "":
            db_file_write = self.write_file()
            db_file_write.write(str(data))
        
    def get(self, id=""):
        db = self.read_file()
        items = eval(db.read())
        
        if id != "":
            return list(filter (lambda person: person['id'] == id, items))
        else:
            return items
            
    def insert(self, data):
        db_read = self.read_file()
        items = eval(db_read.read())
        items.append(data)

        db_write = self.write_file()
        db_write.write(str(items))

        return data

    def update(self, data):
        db_read = self.read_file()
        items = eval(db_read.read())
        item = list(filter(lambda item: item["id"] == data["id"], items))

        if len(item) == 0:
            return {
                "error": True,
                "message": "Item not found!"
            }

        product, = item
        print(product)
        for key in product:
            if key in data:
                product[key] = data[key]

        item_index = items.index(product)

        items[item_index] = product

        db_write = self.write_file()
        db_write.write(str(items))

        return item
    
    def delete(self, id):
        db_read = self.read_file()
        items = eval(db_read.read())

        left_items = list(filter(lambda product: product["id"] != id, items))

        db_write = self.write_file()
        db_write.write(str(left_items))

    def read_file(self):
        return open(self.file, mode="r", encoding="utf-8")
    
    def write_file(self):
        return open(self.file, mode="w", encoding="utf-8")

