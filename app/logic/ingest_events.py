from app.constants import NFT_HOURLY_THRESHOLD, FIRST_NFT_PURCHASE, NFT_VOLUME_THRESHOLD, UNSOLD_NFTS
from app.servicecalls.notification_servicecalls import NotificationServiceCall
from app.db.rules_collection import RulesCollection
from app.db.events_collection import EventsCollection
import concurrent.futures
from app.logger import logger


class IngestEvents:

    # Ingest the events
    @classmethod
    def ingest_events(cls, event):
        cls.execute_rules(event)    
        # cls.execute_rules_concurrently(event)
        EventsCollection.insert_event(event)
        return

    # Execute the rules based on the event
    @classmethod
    def execute_rules(cls, event):
        
        action_map = {
            "check_first_nft_purchase": cls.check_first_nft_purchase,
            "check_nfts_volume": cls.check_nfts_volume,
            "check_nfts_sold" : cls.check_nfts_sold,
        }

        rules = RulesCollection.find_rules({"rule_type": "ingest"})
        rule_set = rules["rule_set"]
        
        # Execute the rules
        for rule in rule_set:
            condition = rule["condition"]
            action = rule["action"]
            
            if action in action_map:
                action_map[action](condition, event)
        return

    @classmethod
    def execute_rules_concurrently(cls, event):
        action_map = {
            "check_first_nft_purchase": cls.check_first_nft_purchase,
            "check_nfts_volume": cls.check_nfts_volume,
            "check_nfts_sold" : cls.check_nfts_sold,
        }

        rules = RulesCollection.find_rules({"rule_type": "ingest"})
        rule_set = rules["rule_set"]
        errors = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(action_map[rule["action"]], rule["condition"], event) for rule in rule_set if rule["action"] in action_map]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    errors.append(e)
        
        if errors:
            for error in errors:
                logger.error(f"Error in executing rules concurrently: {error}")
        return
    
    # Check if the user has made his first NFT purchase
    @classmethod
    def check_first_nft_purchase(cls, condition, event):
        user_id = event.get('userid')
        verb = event.get('verb')
        noun = event.get('noun')
        result = eval(condition, {"verb": verb, "noun": noun})
        if result:
            earlier_nfts = EventsCollection.user_events_count(user_id, verb, noun)
            if not earlier_nfts:
                NotificationServiceCall.notify_user(user_id, FIRST_NFT_PURCHASE)
        return

    # Check if the user has exceeded the hourly threshold of NFTs
    @classmethod
    def check_nfts_volume(cls, condition, event):
        user_id = event.get('userid')
        verb = event.get('verb')
        noun = event.get('noun')
        properties = event.get('properties')
        curr_nfts = properties.get('quantity', 0)

        result = eval(condition, {"verb": verb, "noun": noun, "properties": properties})
        
        if result:
            prev_nfts = EventsCollection.get_nft_volume_by_user(event)
            total_nfts = prev_nfts + curr_nfts
            if total_nfts > NFT_HOURLY_THRESHOLD:
                NotificationServiceCall.notify_operator(NFT_VOLUME_THRESHOLD % (user_id, NFT_HOURLY_THRESHOLD))
        return

    # Check if the user has any unsold NFTs within 
    @classmethod
    def check_nfts_sold(cls, condition, event):
        user_id = event.get('userid')
        verb = event.get('verb')
        noun = event.get('noun')
        result = eval(condition, {"verb": verb, "noun": noun})
        if result:
            unsold_nft_orders = EventsCollection.get_unsold_nft_orders_by_user(event)
            if unsold_nft_orders:
                NotificationServiceCall.notify_user(user_id, UNSOLD_NFTS)
        return
