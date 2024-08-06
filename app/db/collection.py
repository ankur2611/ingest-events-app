from app import mongo_db

class Collection:

    # this method is to get collection instance
    @classmethod
    def get_collection(cls, collection_name):
        return mongo_db.get_collection(collection_name)
