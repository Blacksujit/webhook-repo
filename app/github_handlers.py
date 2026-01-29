def normalize_github_event(event_type, payload):
    if event_type == "push":
        head_commit = payload.get("head_commit", {})
        pusher = payload.get("pusher", {})
        ref = payload.get("ref", "")
        
        # Extract branch name from ref (e.g., "refs/heads/main" -> "main")
        to_branch = ref.replace("refs/heads/", "") if ref.startswith("refs/heads/") else ref
        
        # Ensure request_id is never None - fallback to payload["after"]
        request_id = head_commit.get("id") or payload.get("after")
        
        # Normalize timestamp to ISO-8601 UTC string
        timestamp = head_commit.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = timestamp  # Already ISO format
        elif hasattr(timestamp, 'isoformat'):
            timestamp = timestamp.isoformat()
        
        return {
            "request_id": request_id,
            "author": head_commit.get("author", {}).get("name") or pusher.get("name"),
            "action": "PUSH",
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp
        }
    
    elif event_type == "pull_request":
        action = payload.get("action")
        pull_request = payload.get("pull_request", {})
        
        if action in ("opened", "reopened", "synchronize"):
            # Use created_at if available, fallback to updated_at
            timestamp = pull_request.get("created_at") or pull_request.get("updated_at")
            if isinstance(timestamp, str):
                timestamp = timestamp  # Already ISO format
            elif hasattr(timestamp, 'isoformat'):
                timestamp = timestamp.isoformat()
            
            return {
                "request_id": pull_request.get("id"),
                "author": pull_request.get("user", {}).get("login"),
                "action": "PULL_REQUEST",
                "from_branch": pull_request.get("head", {}).get("ref"),
                "to_branch": pull_request.get("base", {}).get("ref"),
                "timestamp": timestamp
            }
        
        elif action == "closed" and pull_request.get("merged", False):
            # Use merged_at if available, fallback to updated_at
            timestamp = pull_request.get("merged_at") or pull_request.get("updated_at")
            if isinstance(timestamp, str):
                timestamp = timestamp  # Already ISO format
            elif hasattr(timestamp, 'isoformat'):
                timestamp = timestamp.isoformat()
            
            return {
                "request_id": pull_request.get("id"),
                "author": pull_request.get("merged_by", {}).get("login"),
                "action": "MERGE",
                "from_branch": pull_request.get("head", {}).get("ref"),
                "to_branch": pull_request.get("base", {}).get("ref"),
                "timestamp": timestamp
            }
    
    return None