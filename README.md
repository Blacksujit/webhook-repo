# GitHub Webhook Activity Monitor


## Project Overview

This system implements a GitHub webhook listener that captures repository activity and displays it in real-time through a web interface. It listens for push, pull request, and merge events from a monitored repository, normalizes the data, stores it in MongoDB, and presents it through a polling-based dashboard.

## Video Walkthrough
    
[Video Link](https://flonnect.com/video/a0c5c45b210e-470e-a93d-23638b85e8bd)

## Architecture Overview

The system follows a straightforward event-driven architecture: GitHub sends webhook payloads to the Flask backend, which validates, normalizes, and persists events to MongoDB. The frontend polls the backend every 15 seconds for recent events, applying client-side filtering and deduplication to maintain a clean, real-time activity feed.

```mermaid
flowchart TD
    A[action-repo<br/>GitHub Repository] -->|Push/PR/Merge Events| B[GitHub Webhooks]
    B -->|POST /webhook| C[Flask Backend]
    C -->|Signature Verification| D[Event Normalization]
    D -->|Store Events| E[MongoDB Atlas]
    E -->|GET /events| F[UI Dashboard]
    F -->|Poll every 15s| G[Client-side Filtering]
    G -->|Deduplication & Time Window| H[Real-time Activity Display]
```

## Supported GitHub Events

- **Push**: Code commits pushed to any branch
- **Pull Request**: Opened, reopened, or synchronized pull requests
- **Merge**: Pull requests that are merged (bonus feature)

## Merge Event Handling (Bonus)

GitHub does not emit a dedicated merge event. Merge detection is implemented by monitoring pull request webhook events with `action=closed` and `merged=true` in the payload. These events are normalized and stored as `MERGE` actions, providing complete visibility into code integration activities.

## Data Model (MongoDB)

Events are stored with the following schema:

```json
{
  "request_id": "unique_commit_or_pr_id",
  "action": "PUSH|PULL_REQUEST|MERGE",
  "author": "username",
  "from_branch": "feature-branch",
  "to_branch": "main",
  "timestamp": "2026-01-29T22:00:05+05:30"
}
```

- `request_id` ensures uniqueness via MongoDB index
- Timestamps are stored in UTC format
- `from_branch` is null for push events

## Tech Stack

- **Backend**: Flask (Python 3.11+)
- **Database**: MongoDB Atlas with PyMongo
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Integration**: GitHub Webhooks with HMAC-SHA256 signature verification
- **Local Development**: ngrok for webhook tunneling

## Setup Instructions

1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   MONGODB_DB=github_webhooks
   GITHUB_WEBHOOK_SECRET=your_webhook_secret
   FLASK_ENV=development
   ```

3. Run the application:
   ```bash
   python run.py
   ```

4. Access the dashboard at `http://localhost:5000`

## GitHub Webhook Configuration

- **Payload URL**: `https://your-domain.com/webhook`
- **Content type**: `application/json`
- **Events**: Pushes, Pull requests
- **Secret**: Use the same value as `GITHUB_WEBHOOK_SECRET`

## UI Behavior

The dashboard implements intelligent polling and filtering:

- Polls `/events` endpoint every 15 seconds
- Client-side deduplication prevents re-rendering displayed events
- 15-second refresh window filters out stale events
- Events are displayed in chronological order (newest first)


## Design Decisions

**Webhooks over GitHub Actions**: Webhooks provide immediate event notification without requiring repository access or workflow setup, making them ideal for external monitoring systems.

**Client-side deduplication**: Handling deduplication in the UI reduces server load and provides a smoother user experience by avoiding unnecessary DOM manipulation and flickering.

**Merge event handling**: Added merge detection to provide complete visibility into the development lifecycle, as merges represent critical integration points in collaborative workflows.

**Refresh window filtering**: Client-side time-based filtering ensures the UI remains focused on recent activity while maintaining responsiveness and reducing visual clutter.