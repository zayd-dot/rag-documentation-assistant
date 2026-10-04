# System Architecture

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
