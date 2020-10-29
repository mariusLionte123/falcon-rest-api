class Database:
    def __init__(self, data=[]):
        self.data = data

    def get(self, id=""):
        if id != "":
            return list(filter (lambda person: person['id'] == id, self.data))
        else:
            return self.data
            
    def insert(self, data):
        self.data.append(data)

        return data
    def update(self, data):
        for i, user in enumerate(self.data):
            if data["id"] == user["id"]:
                self.data[i] = data
        return data
    
    def delete(self, id):
        self.data = list(filter(lambda person: person["id"] != id, self.data))

