# tests/test_ingest_events.py
import unittest
from unittest.mock import patch
from app.logic.ingest_events import IngestEvents

class TestIngestEvents(unittest.TestCase):

    @patch('app.logic.ingest_events.EventsCollection.insert_event')
    @patch('app.logic.ingest_events.IngestEvents.execute_rules')
    def test_ingest_events(self, mock_execute_rules, mock_insert_event):
        event = {"event": "test_event"}
        IngestEvents.ingest_events(event)
        mock_execute_rules.assert_called_once_with(event)
        mock_insert_event.assert_called_once_with(event)

    @patch('app.logic.ingest_events.RulesCollection.find_rules')
    @patch('app.logic.ingest_events.IngestEvents.check_first_nft_purchase')
    @patch('app.logic.ingest_events.IngestEvents.check_nfts_volume')
    @patch('app.logic.ingest_events.IngestEvents.check_nfts_sold')
    def test_execute_rules(self, mock_check_nfts_sold, mock_check_nfts_volume, mock_check_first_nft_purchase, mock_find_rules):
        event = {"event": "test_event"}
        rules = {
            "rule_set": [
                {"condition": "verb == 'buy'", "action": "check_first_nft_purchase"},
                {"condition": "verb == 'buy'", "action": "check_nfts_volume"},
                {"condition": "verb == 'sell'", "action": "check_nfts_sold"}
            ]
        }
        mock_find_rules.return_value = rules
        IngestEvents.execute_rules(event)
        mock_check_first_nft_purchase.assert_called_once()
        mock_check_nfts_volume.assert_called_once()
        mock_check_nfts_sold.assert_called_once()

    @patch('app.logic.ingest_events.EventsCollection.user_events_count')
    @patch('app.logic.ingest_events.NotificationServiceCall.notify_user')
    def test_check_first_nft_purchase(self, mock_notify_user, mock_user_events_count):
        event = {"userid": "user1", "verb": "buy", "noun": "nft"}
        condition = "verb == 'buy' and noun == 'nft'"
        mock_user_events_count.return_value = 0
        IngestEvents.check_first_nft_purchase(condition, event)
        mock_notify_user.assert_called_once_with("user1", "Congratulations! You have made your first NFT purchase.")

    @patch('app.logic.ingest_events.EventsCollection.get_unsold_nft_orders_by_user')
    @patch('app.logic.ingest_events.NotificationServiceCall.notify_user')
    def test_check_nfts_sold(self, mock_notify_user, mock_get_unsold_nft_orders_by_user):
        event = {"userid": "user1", "verb": "sell", "noun": "nft"}
        condition = "verb == 'sell' and noun == 'nft'"
        mock_get_unsold_nft_orders_by_user.return_value = ["order1"]
        IngestEvents.check_nfts_sold(condition, event)
        mock_notify_user.assert_called_once_with("user1", "You have unsold NFTs in your account")

if __name__ == '__main__':
    unittest.main()
