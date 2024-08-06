from flask import Blueprint, jsonify, request, g
from app.controllers.v1.ingest_controller import IngestController
import time
from app.logger import logger


route_v1 = Blueprint('route_v1', __name__)

# Flask global error handler
@route_v1.errorhandler(Exception)
def global_error_handler(e):
    return jsonify(error=str(e)), 500

# Flask before request
@route_v1.before_request
def before_request():
    g.start_time = time.time()
    

# Flask after request
@route_v1.after_request
def after_request(response):
    perf_diff = (time.time() - g.start_time) * 1000 # in ms
    logger.info(f"Performance: {perf_diff} ms")
    return response

@route_v1.route('/ingest-events', methods=['POST'])
def ingest_events():
    response = IngestController.ingest_events(request)
    return response
