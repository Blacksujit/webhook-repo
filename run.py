from dotenv import load_dotenv
import os
import logging

load_dotenv()

try:
    MONGODB_URI = os.environ.get('MONGODB_URI')
    MONGODB_DB = os.environ.get('MONGODB_DB')
    GITHUB_WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET')
    FLASK_ENV = os.environ.get('FLASK_ENV')

    print(f"Environment loaded:")
    print(f"MongoDB URI: {MONGODB_URI}")
    print(f"Database: {MONGODB_DB}")
    print(f"Flask Env: {FLASK_ENV}")

    if not MONGODB_URI or not MONGODB_DB:
        raise ValueError("MONGODB_URI and MONGODB_DB environment variables must be set")

except Exception as e:
    logging.error(f"Failed to load environment variables: {str(e)}")
    exit(1)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)