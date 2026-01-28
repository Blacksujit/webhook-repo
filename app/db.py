from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError


def init_db(app):
    try:
        mongodb_uri = app.config['MONGODB_URI']
        mongodb_db = app.config['MONGODB_DB']
        
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        db = client[mongodb_db]
        
        # Create unique index on request_id
        events = db.events
        events.create_index("request_id", unique=True)
        
        # Store client and collections in app context
        app.mongo_client = client
        app.events_collection = events
        
    except (ServerSelectionTimeoutError, Exception) as e:
        print(f"Warning: Could not connect to MongoDB: {e}")
        print("App will run without database functionality")
        app.mongo_client = None
        app.events_collection = None


def get_events_collection(app):
    return app.events_collection