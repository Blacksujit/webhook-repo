import hmac
import hashlib
from flask import Blueprint, request, current_app, jsonify
from app.github_handlers import normalize_github_event
from app.db import get_events_collection

webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    # Get signature from header
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return '', 401
    
    # Get the raw request body
    body = request.get_data()
    
    # Get the secret from config
    secret = current_app.config.get('GITHUB_WEBHOOK_SECRET')
    if not secret:
        return '', 401
    
    # Verify signature
    expected_signature = 'sha256=' + hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        return '', 401
    
    # Get event type and parse payload
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.get_json(silent=True)
    if payload is None:
        return '', 200
    
    # Normalize event
    normalized_event = normalize_github_event(event_type, payload)
    if normalized_event is None:
        return '', 200
    
    # Persist to MongoDB
    events_collection = get_events_collection(current_app._get_current_object())
    if events_collection is not None:
        events_collection.update_one(
            {"request_id": normalized_event["request_id"]},
            {"$setOnInsert": normalized_event},
            upsert=True
        )
    
    return '', 200


@webhook_bp.route('/events', methods=['GET'])
def get_events():
    events_collection = get_events_collection(current_app._get_current_object())
    if events_collection is None:
        return jsonify([]), 200
    
    # Fetch events sorted by timestamp descending, limit 20, exclude _id
    events = list(events_collection.find(
        {},
        {"_id": 0}
    ).sort("timestamp", -1).limit(20))
    
    return jsonify(events), 200