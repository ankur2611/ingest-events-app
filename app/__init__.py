import os, pymongo
from dotenv import load_dotenv
from flask import Flask

# load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# connect to MongoDB
mongo_db = (pymongo.MongoClient(os.getenv('MONGO_URI')))[os.getenv('MONGO_DATABASE')]

# initialise Flask app
app = Flask(__name__)

from app.routes.v1.routes import route_v1
app.register_blueprint(route_v1, url_prefix='/api/v1')
