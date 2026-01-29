class GitHubActivityDashboard {
    constructor() {
        this.events = [];
        this.pollingInterval = null;
        this.isPolling = false;
        this.eventsListElement = null;
        this.emptyStateElement = null;
        this.renderedEventIds = new Set();
    }

    async fetchEvents() {
        try {
            const response = await fetch('/events');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const events = await response.json();
            this.handleEventsReceived(events);
            
        } catch (error) {
            console.error('Failed to fetch events:', error);
            this.handleFetchError(error);
        }
    }

    handleEventsReceived(events) {
        this.events = events;
        this.updateLastUpdatedTime();
        this.renderEvents();
    }

    handleFetchError(error) {
        // Handle network errors gracefully
        console.warn('Network error - will retry on next poll');
        
        // Could show user-friendly error message here
        const errorMessage = error.message || 'Unknown error occurred';
        console.error('Fetch error details:', errorMessage);
    }

    updateLastUpdatedTime() {
        const lastUpdatedElement = document.getElementById('last-updated-time');
        if (lastUpdatedElement) {
            const now = new Date();
            lastUpdatedElement.textContent = now.toLocaleTimeString();
        }
    }

    renderEvents() {
        // Initialize DOM elements if not already done
        if (!this.eventsListElement) {
            this.eventsListElement = document.getElementById('events-list');
        }
        if (!this.emptyStateElement) {
            this.emptyStateElement = document.getElementById('empty-state');
        }

        // Show empty state if no events
        if (!this.events || this.events.length === 0) {
            if (this.emptyStateElement) {
                this.emptyStateElement.style.display = 'block';
            }
            if (this.eventsListElement) {
                this.eventsListElement.style.display = 'none';
            }
            return;
        }

        // Hide empty state and show events
        if (this.emptyStateElement) {
            this.emptyStateElement.style.display = 'none';
        }
        if (this.eventsListElement) {
            this.eventsListElement.style.display = 'grid';
        }

        // Render only new events (not already rendered)
        this.events.forEach(event => {
            if (!this.renderedEventIds.has(event.request_id)) {
                const eventCard = this.createEventCard(event);
                if (this.eventsListElement) {
                    this.eventsListElement.appendChild(eventCard);
                }
                this.renderedEventIds.add(event.request_id);
            }
        });
    }

    createEventCard(event) {
        const formattedEvent = formatGitHubEvent(event);
        
        // Create event card container
        const card = document.createElement('div');
        card.className = 'event-card';
        card.setAttribute('data-event-type', formattedEvent.eventType);

        // Create event header
        const header = document.createElement('div');
        header.className = 'event-header';

        // Create event type badge
        const typeBadge = document.createElement('span');
        typeBadge.className = 'event-type';
        typeBadge.textContent = formattedEvent.eventType.toUpperCase();

        // Create timestamp
        const timestamp = document.createElement('span');
        timestamp.className = 'event-timestamp';
        timestamp.textContent = formattedEvent.formattedTimestamp;

        // Assemble header
        header.appendChild(typeBadge);
        header.appendChild(timestamp);

        // Create event content
        const content = document.createElement('div');
        content.className = 'event-content';

        // Create author
        const author = document.createElement('div');
        author.className = 'event-author';
        author.textContent = formattedEvent.displayText;

        // Create branch information if available
        if (event.from_branch || event.to_branch) {
            const branches = document.createElement('div');
            branches.className = 'event-branches';

            if (event.from_branch) {
                const fromBranch = document.createElement('span');
                fromBranch.className = 'branch-name';
                fromBranch.textContent = event.from_branch;
                branches.appendChild(fromBranch);
            }

            if (event.from_branch && event.to_branch) {
                const arrow = document.createElement('span');
                arrow.className = 'branch-arrow';
                arrow.textContent = '→';
                branches.appendChild(arrow);
            }

            if (event.to_branch) {
                const toBranch = document.createElement('span');
                toBranch.className = 'branch-name';
                toBranch.textContent = event.to_branch;
                branches.appendChild(toBranch);
            }

            content.appendChild(branches);
        }

        content.appendChild(author);

        // Assemble card
        card.appendChild(header);
        card.appendChild(content);

        return card;
    }

    startPolling() {
        if (this.isPolling) {
            return;
        }

        this.isPolling = true;
        
        // Initial fetch
        this.fetchEvents();
        
        // Set up polling every 15 seconds
        this.pollingInterval = setInterval(() => {
            this.fetchEvents();
        }, 15000);
    }

    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
        
        this.isPolling = false;
    }

    // Public method to get current events
    getEvents() {
        return this.events;
    }
}

// Pure formatting layer for GitHub events
function formatGitHubEvent(event) {
    const { action, author, from_branch, to_branch, timestamp } = event;
    
    let eventType;
    let displayText;
    
    // Format timestamp to human readable UTC
    const formattedTimestamp = new Date(timestamp).toUTCString();
    
    switch (action) {
        case 'PUSH':
            eventType = 'push';
            displayText = `${author} pushed to ${to_branch} on ${formattedTimestamp}`;
            break;
            
        case 'PULL_REQUEST':
            eventType = 'pr';
            displayText = `${author} submitted a pull request from ${from_branch} to ${to_branch} on ${formattedTimestamp}`;
            break;
            
        case 'MERGE':
            eventType = 'merge';
            displayText = `${author} merged branch ${from_branch} to ${to_branch} on ${formattedTimestamp}`;
            break;
            
        default:
            eventType = 'unknown';
            displayText = `${author} performed ${action} on ${formattedTimestamp}`;
    }
    
    return {
        displayText,
        eventType,
        formattedTimestamp
    };
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new GitHubActivityDashboard();
    dashboard.startPolling();
    
    // Make dashboard instance available globally for debugging
    window.dashboard = dashboard;
    window.formatGitHubEvent = formatGitHubEvent;
});