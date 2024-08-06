import time
from app.db.collection import Collection

class EventsCollection(Collection):

    collection_instance = None
    collection_name = "events"

    @classmethod
    def get_nft_volume_by_user(cls, event):

        if cls.collection_instance is None:
            cls.collection_instance = cls.get_collection(cls.collection_name)

        user_id = event.get('userid')
        verb = event.get('verb')
        noun = event.get('noun')
        event_timestamp = event.get('timestamp')
        current_timestamp = int(time.time())
        one_hour_ago = current_timestamp - 3600
        
        pipeline = [
            {"$match": {"userid": user_id, "verb": verb, "noun": noun, "timestamp": {"$gte": one_hour_ago, "$lte": event_timestamp}}},
            {"$group": {"_id": None, "total": {"$sum": "$properties.quantity"}}}
        ]
        
        data = list(cls.collection_instance.aggregate(pipeline))
        if len(data):
            return data[0].get('total')

        return 0

    @classmethod
    def user_events_count(cls, user_id, verb, noun):
        if cls.collection_instance is None:
            cls.collection_instance = cls.get_collection(cls.collection_name)

        return cls.collection_instance.count_documents({"userid": user_id, "verb": verb, "noun": noun})

    @classmethod
    def insert_event(cls, event):
        if cls.collection_instance is None:
            cls.collection_instance = cls.get_collection(cls.collection_name)

        cls.collection_instance.insert_one(event)
    

    @classmethod
    def get_unsold_nft_orders_by_user(cls, event):

        if cls.collection_instance is None:
            cls.collection_instance = cls.get_collection(cls.collection_name)

        user_id = event.get('userid')
        verb = event.get('verb')
        noun = event.get('noun')
        current_timestamp = int(time.time())
        seven_days_ago = current_timestamp - 7 * 24 * 3600

        query = {"userid": user_id, "verb": verb, "noun": noun, "timestamp": {"$lte": seven_days_ago}}
        return cls.collection_instance.count_documents(query)