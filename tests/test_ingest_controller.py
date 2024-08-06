# tests/test_ingest_events_controller.py
import unittest
from unittest.mock import patch
from app import app

class TestIngestEventsController(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.logic.ingest_events.IngestEvents.ingest_events')
    def test_ingest_event_success(self, mock_ingest_events):
        mock_ingest_events.return_value = None
        response = self.app.post('/api/v1/ingest-events', json={"event": "test_event"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Events ingested successfully', 'status': 'success'})

    @patch('app.logic.ingest_events.IngestEvents.ingest_events')
    def test_ingest_event_failure(self, mock_ingest_events):
        mock_ingest_events.side_effect = Exception("Test exception")
        response = self.app.post('/api/v1/ingest-events', json={"event": "test_event"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {'error': 'Test exception'})

if __name__ == '__main__':
    unittest.main()
