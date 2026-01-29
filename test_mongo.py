import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_DB = os.environ.get('MONGODB_DB')

print(f"Testing MongoDB connection...")
print(f"URI: {MONGODB_URI}")
print(f"DB: {MONGODB_DB}")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
    
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # Test database access
    db = client[MONGODB_DB]
    print(f"✅ Database '{MONGODB_DB}' accessible!")
    
    # Test collection creation
    test_collection = db.test_connection
    test_collection.insert_one({"test": "connection"})
    print("✅ Can write to database!")
    
    # Clean up
    test_collection.drop()
    print("✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    
    # Common issues and solutions
    if "authentication failed" in str(e):
        print("\n🔧 Possible solutions:")
        print("1. Check username and password in MongoDB Atlas")
        print("2. Ensure user has read/write permissions for the database")
        print("3. Verify the password doesn't contain special characters that need URL encoding")
    elif "timeout" in str(e):
        print("\n🔧 Possible solutions:")
        print("1. Check network connectivity")
        print("2. Verify IP whitelist in MongoDB Atlas")
        print("3. Check cluster name and region")
    elif "bad auth" in str(e):
        print("\n🔧 Possible solutions:")
        print("1. Username or password is incorrect")
        print("2. User may not exist in this cluster")
        print("3. Password may need URL encoding for special characters")
