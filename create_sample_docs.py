"""Generate sample technical documents for testing."""
import os

DOCS_DIR = "data/documents"
os.makedirs(DOCS_DIR, exist_ok=True)

docs = {
    "api_guide.md": """# API Reference Guide

## Authentication
All API requests require a Bearer token in the Authorization header.
Tokens expire after 24 hours and must be refreshed using the /auth/refresh endpoint.

### Rate Limiting
The API enforces rate limits of 100 requests per minute per API key.
Exceeding this limit returns a 429 Too Many Requests response.
Implement exponential backoff with a maximum of 3 retries.

## Endpoints

### GET /api/v1/users
Returns a paginated list of users. Supports filtering by role, status, and creation date.
Default page size is 20, maximum is 100.

### POST /api/v1/users
Creates a new user. Required fields: email, name, role.
Returns 201 Created with the user object on success.
Returns 409 Conflict if the email already exists.

## Error Handling
All errors return a JSON object with 'error' and 'message' fields.
Common error codes: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 500 (server error).
""",

    "deployment_guide.md": """# Deployment Guide

## Prerequisites
- Docker 20.10+
- Kubernetes 1.24+ (for production)
- PostgreSQL 14+
- Redis 7+

## Environment Variables
- DATABASE_URL: PostgreSQL connection string
- REDIS_URL: Redis connection string
- SECRET_KEY: Application secret key (min 32 characters)
- LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
- MAX_WORKERS: Number of Gunicorn workers (default: 4)

## Local Development
Run docker-compose up -d, then python manage.py migrate, then python manage.py runserver.

## Production Deployment
1. Build the Docker image
2. Push to container registry
3. Apply Kubernetes manifests
4. Run database migrations

## Health Checks
The application exposes /health and /ready endpoints.
/health returns 200 if the process is running.
/ready returns 200 if the app can connect to database and Redis.

## Troubleshooting
If the app fails to start, check DATABASE_URL and REDIS_URL connectivity.
For high memory usage, reduce MAX_WORKERS.
For slow queries, enable query logging with LOG_LEVEL=DEBUG.
""",

    "architecture.md": """# System Architecture

## Overview
The system follows a microservices architecture with an API Gateway pattern.
Services communicate via REST APIs for synchronous calls and RabbitMQ for async events.

## Components

### API Gateway
Routes requests to appropriate microservices.
Handles authentication and rate limiting.
Implements circuit breaker pattern for fault tolerance.
Built with Kong Gateway.

### User Service
Manages user accounts, authentication, and authorization.
Uses JWT tokens with RS256 signing.
Stores data in PostgreSQL.
Caches sessions in Redis with 24-hour TTL.

### Order Service
Processes orders and manages order lifecycle.
Implements saga pattern for distributed transactions.
Publishes events to RabbitMQ on state changes.
Uses event sourcing for audit trail.

### Notification Service
Sends emails, SMS, and push notifications.
Consumes events from RabbitMQ.
Uses template engine for message formatting.

## Security
All inter-service communication uses mTLS.
Secrets managed via HashiCorp Vault.
Database encryption at rest using AES-256.
""",
}

for fname, content in docs.items():
    with open(os.path.join(DOCS_DIR, fname), "w") as f:
        f.write(content)
    print(f"Created {fname}")
print(f"\nGenerated {len(docs)} sample documents in {DOCS_DIR}/")
