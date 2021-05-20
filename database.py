import pymongo

class Database(pymongo.MongoClient):

    HOST = "127.0.0.1"
    COLLECTIONS = ["members", "events", "afk"]

    def __init__(self, tag: str, **kwargs):

        # If the tag supplied is in the form '[TAG]', then remove the square brackets
        self.tag = tag.replace("[", "").replace("]", "")
        host = kwargs.get("host", self.HOST)
        super().__init__(
            host, 
            **kwargs
        )
        self._create_database(name=self.tag)

    @classmethod
    def create(cls, tag :str, **kwargs):

        Database.__init__(cls, tag=tag, **kwargs)._create_database(name=cls.tag)
        return cls

    def __call__(self):

        return self[self.tag]

    def _create_database(self, name: str):
        
        for collection in self.COLLECTIONS:
            try:
                self[name].create_collection(collection)
            except pymongo.errors.CollectionInvalid:
                pass


if __name__ == "__main__":

    database = Database(tag="[BJay]")