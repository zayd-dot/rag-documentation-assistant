# Deployment Guide

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
