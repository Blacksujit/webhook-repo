from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def init_db(app):
    mongodb_uri = app.config['MONGODB_URI']
    mongodb_db = app.config['MONGODB_DB']
    
    client = MongoClient(mongodb_uri)
    db = client[mongodb_db]
    
    # Create unique index on request_id
    events = db.events
    events.create_index("request_id", unique=True)
    
    # Store client and collections in app context
    app.mongo_client = client
    app.events_collection = events


def get_events_collection(app):
    return app.events_collection