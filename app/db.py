from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


_client = None


def get_client(app):
    global _client
    if _client is None:
        mongodb_uri = app.config['MONGODB_URI']
        _client = MongoClient(mongodb_uri)
    return _client


def get_db(app):
    client = get_client(app)
    mongodb_db = app.config['MONGODB_DB']
    return client[mongodb_db]


def get_events_collection(app):
    db = get_db(app)
    events = db.events
    
    # Ensure unique index on request_id
    events.create_index("request_id", unique=True)
    
    return events