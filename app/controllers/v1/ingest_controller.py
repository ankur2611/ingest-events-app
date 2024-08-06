from flask import jsonify
from app.logic.ingest_events import IngestEvents


class IngestController:

    @classmethod
    def ingest_events(cls, request):
        data = request.json
        IngestEvents.ingest_events(data)
        return jsonify({'status': 'success', 'message': 'Events ingested successfully'})
