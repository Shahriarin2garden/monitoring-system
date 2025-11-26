# Prometheus Queries Reference

Complete guide to PromQL queries for monitoring the API system.

## Quick Reference

### Request Rate
```promql
rate(http_requests_total[5m])
```

### Error Rate
```promql
(rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) * 100
```

### P95 Latency
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

## Basic Queries

### Total Requests (All Time)
```promql
http_requests_total
```

Returns the total count of all HTTP requests since the API started.

---

### Current Active Requests
```promql
http_requests_in_progress
```

Shows the number of requests currently being processed.

---

### Total Errors (All Time)
```promql
api_errors_total
```

Returns the total count of all API errors since the API started.

---

## Rate Queries (5-minute window)

### Request Rate (Requests per Second)
```promql
rate(http_requests_total[5m])
```

Shows how many requests per second the API is handling.

**Breakdown by Method:**
```promql
rate(http_requests_total[5m]) by (method)
```

**Breakdown by Route:**
```promql
rate(http_requests_total[5m]) by (route)
```

**Breakdown by Status:**
```promql
rate(http_requests_total[5m]) by (status)
```

---

### Error Rate (Errors per Second)
```promql
rate(api_errors_total[5m])
```

Shows how many errors per second are occurring.

**By Error Type:**
```promql
rate(api_errors_total[5m]) by (error_type)
```

---

### 5xx Error Rate (Server Errors per Second)
```promql
rate(http_requests_total{status=~"5.."}[5m])
```

Shows only server errors (5xx status codes).

---

### 4xx Error Rate (Client Errors per Second)
```promql
rate(http_requests_total{status=~"4.."}[5m])
```

Shows only client errors (4xx status codes).

---

## Error Rate Percentage

### Overall Error Rate (%)
```promql
(rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) * 100
```

Percentage of requests that resulted in 5xx errors.

---

### Error Rate by Endpoint (%)
```promql
(rate(http_requests_total{status=~"5..",route=~"/api/.*"}[5m]) / rate(http_requests_total{route=~"/api/.*"}[5m])) * 100
```

Error rate for specific endpoints.

---

## Latency Queries

### Average Response Time (Seconds)
```promql
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

Average latency across all requests.

---

### Average Response Time (Milliseconds)
```promql
(rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])) * 1000
```

Same as above but in milliseconds for easier reading.

---

### P50 Latency (Median)
```promql
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))
```

50th percentile - half of requests are faster than this.

---

### P95 Latency
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

95th percentile - 95% of requests are faster than this.

---

### P99 Latency
```promql
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

99th percentile - 99% of requests are faster than this.

---

### P99.9 Latency
```promql
histogram_quantile(0.999, rate(http_request_duration_seconds_bucket[5m]))
```

99.9th percentile - for tracking tail latency.

---

### Max Latency (Approximate)
```promql
histogram_quantile(1.0, rate(http_request_duration_seconds_bucket[5m]))
```

Approximate maximum latency (based on histogram buckets).

---

### Latency by Endpoint
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) by (route)
```

P95 latency for each endpoint.

---

### Latency by Method
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) by (method)
```

P95 latency for each HTTP method.

---

## Request Distribution

### Requests by Status Code
```promql
sum by (status) (rate(http_requests_total[5m]))
```

Shows distribution of requests across different HTTP status codes.

---

### Requests by Endpoint
```promql
sum by (route) (rate(http_requests_total[5m]))
```

Shows which endpoints are receiving the most traffic.

---

### Requests by Method
```promql
sum by (method) (rate(http_requests_total[5m]))
```

Shows distribution across GET, POST, PUT, DELETE, etc.

---

### Top 5 Endpoints by Request Rate
```promql
topk(5, sum by (route) (rate(http_requests_total[5m])))
```

Shows the 5 most frequently called endpoints.

---

### Bottom 5 Endpoints by Request Rate
```promql
bottomk(5, sum by (route) (rate(http_requests_total[5m])))
```

Shows the 5 least frequently called endpoints.

---

## Performance Analysis

### Slowest Endpoints (P95)
```promql
topk(5, histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) by (route))
```

Shows the 5 endpoints with highest P95 latency.

---

### Fastest Endpoints (P95)
```promql
bottomk(5, histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) by (route))
```

Shows the 5 endpoints with lowest P95 latency.

---

### Endpoints with Most Errors
```promql
topk(5, sum by (route) (rate(http_requests_total{status=~"5.."}[5m])))
```

Shows endpoints with the most 5xx errors.

---

## Time Window Variations

All queries above use `[5m]` (5-minute window). You can adjust:

- `[1m]` - 1 minute (more responsive, noisier)
- `[5m]` - 5 minutes (balanced)
- `[15m]` - 15 minutes (smoother, less responsive)
- `[1h]` - 1 hour (very smooth, slow to respond)

**Example with 1-minute window:**
```promql
rate(http_requests_total[1m])
```

**Example with 1-hour window:**
```promql
rate(http_requests_total[1h])
```

---

## Advanced Queries

### Request Rate with Offset (Compare to 1 hour ago)
```promql
rate(http_requests_total[5m]) - rate(http_requests_total[5m] offset 1h)
```

Shows how request rate has changed compared to 1 hour ago.

---

### Error Rate Trend
```promql
(rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) * 100
```

Shows error rate trend over time.

---

### Request Throughput (Requests per Minute)
```promql
rate(http_requests_total[5m]) * 60
```

Shows requests per minute instead of per second.

---

### Request Throughput (Requests per Hour)
```promql
rate(http_requests_total[5m]) * 3600
```

Shows requests per hour.

---

### Successful Requests Rate
```promql
rate(http_requests_total{status=~"2.."}[5m])
```

Shows only successful requests (2xx status codes).

---

### Redirect Rate
```promql
rate(http_requests_total{status=~"3.."}[5m])
```

Shows redirect responses (3xx status codes).

---

### Total Requests in Last Hour
```promql
increase(http_requests_total[1h])
```

Total number of requests in the last hour.

---

### Total Errors in Last Hour
```promql
increase(api_errors_total[1h])
```

Total number of errors in the last hour.

---

## Alerting Queries

### High Error Rate Alert (>5%)
```promql
(rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) * 100 > 5
```

Triggers when error rate exceeds 5%.

---

### High Latency Alert (P95 > 1 second)
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
```

Triggers when P95 latency exceeds 1 second.

---

### No Requests Alert
```promql
rate(http_requests_total[5m]) == 0
```

Triggers when no requests are being received.

---

### High Active Requests Alert (>10)
```promql
http_requests_in_progress > 10
```

Triggers when more than 10 requests are in progress.

---

## Grafana Dashboard Queries

### Panel: Request Rate
```promql
rate(http_requests_total[5m])
```

Legend: `{{method}} {{route}}`

---

### Panel: Error Rate
```promql
(rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) * 100
```

Legend: `Error Rate`

---

### Panel: Latency Percentiles
```promql
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

Legend: `P50 {{method}} {{route}}`, `P95 {{method}} {{route}}`, `P99 {{method}} {{route}}`

---

### Panel: Active Requests
```promql
http_requests_in_progress
```

Legend: `{{method}} {{route}}`

---

### Panel: Requests by Status
```promql
sum by (status) (rate(http_requests_total[5m]))
```

Legend: `Status {{status}}`

---

### Panel: Errors by Type
```promql
rate(api_errors_total[5m])
```

Legend: `{{error_type}}`

---

### Panel: Request Distribution
```promql
sum by (route) (rate(http_requests_total[5m]))
```

Legend: `{{route}}`

---

### Panel: Average Response Time
```promql
(rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])) * 1000
```

Legend: `{{method}} {{route}}`

---

## Testing Queries

### Verify Metrics are Being Collected
```promql
http_requests_total
```

Should return non-zero values if traffic has been generated.

---

### Check Slow Endpoint Latency
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{route="/api/slow"}[5m]))
```

Should show ~2-3 seconds for the slow endpoint.

---

### Check Error Endpoint Errors
```promql
rate(http_requests_total{route="/api/error",status="500"}[5m])
```

Should show errors from the error endpoint.

---

## Tips & Tricks

### Use `by` for Grouping
```promql
sum by (route) (rate(http_requests_total[5m]))
```

Groups results by the specified label.

---

### Use `without` for Excluding Labels
```promql
sum without (status) (rate(http_requests_total[5m]))
```

Sums across all status codes.

---

### Use `topk` for Top N Results
```promql
topk(10, rate(http_requests_total[5m]))
```

Shows top 10 results.

---

### Use `bottomk` for Bottom N Results
```promql
bottomk(5, rate(http_requests_total[5m]))
```

Shows bottom 5 results.

---

### Use `on` for Label Matching
```promql
rate(http_requests_total[5m]) on (route) group_left() http_requests_in_progress
```

Joins metrics on matching labels.

---

## Common Mistakes

### ❌ Forgetting Time Window
```promql
rate(http_requests_total)  # Wrong - no time window
```

### ✅ Correct
```promql
rate(http_requests_total[5m])  # Correct - includes time window
```

---

### ❌ Using `sum` Instead of `rate`
```promql
sum(http_requests_total)  # Wrong - returns total, not rate
```

### ✅ Correct
```promql
rate(http_requests_total[5m])  # Correct - returns rate
```

---

### ❌ Forgetting Regex Syntax
```promql
http_requests_total{status="5.."}  # Wrong - not regex
```

### ✅ Correct
```promql
http_requests_total{status=~"5.."}  # Correct - uses regex
```

---

## Resources

- [Prometheus Query Language](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [PromQL Functions](https://prometheus.io/docs/prometheus/latest/querying/functions/)
- [Histogram Quantiles](https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile)

---

**Last Updated:** 2024
**Prometheus Version:** 2.x+
