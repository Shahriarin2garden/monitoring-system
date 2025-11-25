# API Documentation

Complete reference for all REST API endpoints in the monitoring system.

## Base URL

```
http://localhost:8000
```

## Health & System Endpoints

### Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "service": "api-monitoring"
}
```

**Status Code:** 200 OK

---

### Prometheus Metrics

**Endpoint:** `GET /metrics`

**Description:** Expose all metrics in Prometheus text format. Used by Prometheus scraper.

**Response:** Prometheus text format
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",route="/api/users",status="200"} 42.0

# HELP http_request_duration_seconds HTTP request latency in seconds
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{method="GET",route="/api/users",le="0.005"} 5.0
...
```

**Status Code:** 200 OK

**Content-Type:** `text/plain; charset=utf-8`

---

## User Management Endpoints

### List All Users

**Endpoint:** `GET /api/users`

**Description:** Retrieve all users in the system.

**Query Parameters:** None

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ],
  "count": 2
}
```

**Status Code:** 200 OK

**Example:**
```bash
curl http://localhost:8000/api/users
```

---

### Get User by ID

**Endpoint:** `GET /api/users/{id}`

**Description:** Retrieve a specific user by their ID.

**Path Parameters:**
- `id` (integer, required): User ID

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Status Codes:**
- 200 OK - User found
- 404 Not Found - User does not exist

**Example:**
```bash
curl http://localhost:8000/api/users/1
```

**Error Response (404):**
```json
{
  "detail": "User not found"
}
```

---

### Create User

**Endpoint:** `POST /api/users`

**Description:** Create a new user.

**Query Parameters:**
- `name` (string, required): User's full name
- `email` (string, required): User's email address

**Response:**
```json
{
  "id": 3,
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

**Status Code:** 200 OK

**Example:**
```bash
curl -X POST "http://localhost:8000/api/users?name=Alice%20Johnson&email=alice@example.com"
```

**Metrics Tracked:**
- `http_requests_total{method="POST",route="/api/users",status="200"}`
- `http_request_duration_seconds{method="POST",route="/api/users"}`

---

### Update User

**Endpoint:** `PUT /api/users/{id}`

**Description:** Update an existing user's information.

**Path Parameters:**
- `id` (integer, required): User ID

**Query Parameters:**
- `name` (string, optional): New user name
- `email` (string, optional): New email address

**Response:**
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "john.smith@example.com"
}
```

**Status Codes:**
- 200 OK - User updated
- 404 Not Found - User does not exist

**Example:**
```bash
curl -X PUT "http://localhost:8000/api/users/1?name=John%20Smith&email=john.smith@example.com"
```

**Error Response (404):**
```json
{
  "detail": "User not found"
}
```

---

### Delete User

**Endpoint:** `DELETE /api/users/{id}`

**Description:** Delete a user from the system.

**Path Parameters:**
- `id` (integer, required): User ID

**Response:**
```json
{
  "message": "User deleted",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Status Codes:**
- 200 OK - User deleted
- 404 Not Found - User does not exist

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/users/1
```

**Error Response (404):**
```json
{
  "detail": "User not found"
}
```

---

## Testing Endpoints

### Slow Endpoint

**Endpoint:** `GET /api/slow`

**Description:** Simulated slow endpoint that takes 2-3 seconds to respond. Useful for testing latency metrics.

**Response:**
```json
{
  "message": "Slow endpoint response",
  "delay_seconds": 2.456
}
```

**Status Code:** 200 OK

**Expected Latency:** 2-3 seconds

**Example:**
```bash
curl http://localhost:8000/api/slow
```

**Metrics Tracked:**
- `http_request_duration_seconds{method="GET",route="/api/slow"}` - Will show high latency
- `http_requests_in_progress{method="GET",route="/api/slow"}` - Will show active requests

---

### Error Endpoint

**Endpoint:** `GET /api/error`

**Description:** Simulated error endpoint that always returns a 500 error. Useful for testing error tracking.

**Response:**
```json
{
  "detail": "Simulated API error"
}
```

**Status Code:** 500 Internal Server Error

**Example:**
```bash
curl http://localhost:8000/api/error
```

**Metrics Tracked:**
- `http_requests_total{method="GET",route="/api/error",status="500"}` - Error counter
- `api_errors_total{error_type="HTTPException"}` - Error type tracking

---

## Legacy Endpoints (Backward Compatible)

### Update Active Users

**Endpoint:** `GET /update`

**Description:** Update the active user count metric (legacy endpoint).

**Query Parameters:**
- `users` (integer, required): Number of active users (must be ≥ 0)

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- 200 OK - Updated successfully
- 400 Bad Request - Invalid users count

**Example:**
```bash
curl "http://localhost:8000/update?users=42"
```

**Error Response (400):**
```json
{
  "detail": "Users cannot be negative"
}
```

---

### Update CPU Usage

**Endpoint:** `GET /cpu`

**Description:** Update the CPU usage metric (legacy endpoint).

**Query Parameters:**
- `value` (float, required): CPU usage percentage (0-100)

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- 200 OK - Updated successfully
- 400 Bad Request - Invalid CPU value

**Example:**
```bash
curl "http://localhost:8000/cpu?value=65.5"
```

**Error Response (400):**
```json
{
  "detail": "CPU must be 0–100"
}
```

---

## Metrics Reference

### HTTP Request Metrics

#### http_requests_total
- **Type:** Counter
- **Description:** Total number of HTTP requests
- **Labels:** `method`, `route`, `status`
- **Example:** `http_requests_total{method="GET",route="/api/users",status="200"}`

#### http_request_duration_seconds
- **Type:** Histogram
- **Description:** HTTP request latency in seconds
- **Labels:** `method`, `route`
- **Buckets:** 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0
- **Example:** `http_request_duration_seconds_bucket{method="GET",route="/api/users",le="0.1"}`

#### http_requests_in_progress
- **Type:** Gauge
- **Description:** Number of active HTTP requests
- **Labels:** `method`, `route`
- **Example:** `http_requests_in_progress{method="GET",route="/api/users"}`

#### api_errors_total
- **Type:** Counter
- **Description:** Total number of API errors
- **Labels:** `error_type`
- **Example:** `api_errors_total{error_type="HTTPException"}`

### Legacy Metrics

#### app_requests_total
- **Type:** Counter
- **Description:** Total API requests (legacy)

#### app_active_users
- **Type:** Gauge
- **Description:** Active user count (legacy)

#### app_cpu_usage_percent
- **Type:** Gauge
- **Description:** CPU usage percentage (legacy)

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid query parameters |
| 404 | Not Found | User ID doesn't exist |
| 500 | Internal Server Error | Simulated error endpoint |

### Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. All endpoints accept unlimited requests.

---

## Authentication

Currently, there is no authentication required. All endpoints are publicly accessible.

---

## CORS

CORS is not explicitly configured. The API is designed for internal use within Docker containers.

---

## Request/Response Examples

### Complete User Creation Flow

```bash
# 1. Create first user
curl -X POST "http://localhost:8000/api/users?name=John&email=john@example.com"
# Response: {"id": 1, "name": "John", "email": "john@example.com"}

# 2. Create second user
curl -X POST "http://localhost:8000/api/users?name=Jane&email=jane@example.com"
# Response: {"id": 2, "name": "Jane", "email": "jane@example.com"}

# 3. List all users
curl http://localhost:8000/api/users
# Response: {"users": [...], "count": 2}

# 4. Get specific user
curl http://localhost:8000/api/users/1
# Response: {"id": 1, "name": "John", "email": "john@example.com"}

# 5. Update user
curl -X PUT "http://localhost:8000/api/users/1?name=John%20Doe"
# Response: {"id": 1, "name": "John Doe", "email": "john@example.com"}

# 6. Delete user
curl -X DELETE http://localhost:8000/api/users/1
# Response: {"message": "User deleted", "user": {...}}
```

### Load Testing Flow

```bash
# 1. Generate traffic with slow endpoint
for i in {1..10}; do
  curl http://localhost:8000/api/slow &
done
wait

# 2. Generate errors
for i in {1..5}; do
  curl http://localhost:8000/api/error &
done
wait

# 3. View metrics
curl http://localhost:8000/metrics | grep http_request_duration_seconds
```

---

## Performance Considerations

### Endpoint Performance

| Endpoint | Typical Latency | Notes |
|----------|-----------------|-------|
| `/api/users` | 1-5ms | Fast list operation |
| `/api/users/{id}` | 1-5ms | Fast lookup |
| `/api/users` (POST) | 1-5ms | Fast create |
| `/api/users/{id}` (PUT) | 1-5ms | Fast update |
| `/api/users/{id}` (DELETE) | 1-5ms | Fast delete |
| `/api/slow` | 2000-3000ms | Intentionally slow |
| `/api/error` | 1-5ms | Fast error response |
| `/health` | 1-5ms | Fast health check |
| `/metrics` | 5-20ms | Depends on metric count |

### Metrics Overhead

- Each request adds minimal overhead (~1-2ms)
- Metrics collection is non-blocking
- Prometheus scraping happens every 15 seconds

---

## Troubleshooting

### API Not Responding

```bash
# Check if API is running
curl http://localhost:8000/health

# Check logs
docker-compose logs api
```

### Metrics Not Appearing

```bash
# Generate traffic first
curl http://localhost:8000/api/users

# Wait 15-30 seconds for Prometheus to scrape

# Check raw metrics
curl http://localhost:8000/metrics
```

### User Not Found

```bash
# List all users to see valid IDs
curl http://localhost:8000/api/users

# Use a valid ID
curl http://localhost:8000/api/users/1
```

---

## API Versioning

Currently, there is no API versioning. All endpoints are v1 (implicit).

---

## Changelog

### Version 1.0 (Current)
- Initial release
- CRUD endpoints for users
- Comprehensive metrics collection
- Health check endpoint
- Testing endpoints (slow, error)
- Legacy endpoints for backward compatibility

---

## Support

For issues or questions:
1. Check the README.md for general information
2. Review QUICKSTART.md for common tasks
3. Check docker-compose logs for errors
4. Verify Prometheus targets at http://localhost:9090/targets

---

**Last Updated:** 2024
**API Version:** 1.0
