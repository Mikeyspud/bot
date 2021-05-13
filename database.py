import pymongo

class Database(pymongo.MongoClient):

    host = "127.0.0.1"
    username = "bjay"
    password = "bjay"
    authSource = "bjay"

    def __init__(self):

        super().__init__(self.host, 
                        username=self.username, 
                        password=self.password,
                        authSource=self.authSource)

    def get_member(_id: int) -> dict:

        return self.bjay.members.find_one({"_id": _id})

if __name__ == "__main__":

    database = Database().bjay
    test = database.members.find_one({"test": "123"})