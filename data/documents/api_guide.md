# API Reference Guide

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
