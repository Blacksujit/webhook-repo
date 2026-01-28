import hmac
import hashlib
from flask import Blueprint, request, jsonify

webhook_bp = Blueprint('webhook', __name__)


@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    # Get signature from header
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return jsonify({'error': 'Missing signature'}), 401
    
    # Get the raw request body
    body = request.data
    
    # Get the secret from config
    secret = request.app.config.get('GITHUB_WEBHOOK_SECRET')
    if not secret:
        return jsonify({'error': 'Missing webhook secret'}), 500
    
    # Verify signature
    expected_signature = 'sha256=' + hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Get event type
    event_type = request.headers.get('X-GitHub-Event')
    print(f"Received GitHub event: {event_type}")
    
    # Return success
    return jsonify({'status': 'received'}), 200