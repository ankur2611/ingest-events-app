from app.db.collection import Collection

class RulesCollection(Collection):

    collection_instance = None
    collection_name = "rules"

    @classmethod
    def find_rules(cls, query):

        if cls.collection_instance is None:
            cls.collection_instance = cls.get_collection(cls.collection_name)

        return cls.collection_instance.find_one(query)

