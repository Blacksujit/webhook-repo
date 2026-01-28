import hmac
import hashlib
from flask import Blueprint, request, current_app

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
    
    # Get event type
    event_type = request.headers.get('X-GitHub-Event')
    print(f"Received GitHub event: {event_type}")
    
    # Return success
    return '', 200