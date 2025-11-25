# Quick Start Guide

Get the monitoring system up and running in 5 minutes!

## 1️⃣ Start the System

```bash
docker-compose up -d
```

Wait for all services to be healthy (30-60 seconds):

```bash
docker-compose ps
```

Expected output:
```
NAME                    STATUS
api-monitoring          Up (healthy)
prometheus-monitoring   Up (healthy)
grafana-monitoring      Up (healthy)
```

## 2️⃣ Verify Services

### API Health
```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "healthy", "service": "api-monitoring"}
```

### Prometheus
Visit http://localhost:9090 in your browser

### Grafana
Visit http://localhost:3000 in your browser
- Username: `admin`
- Password: `admin`

## 3️⃣ Generate Traffic

### Option A: Python Script (Recommended)
```bash
python load_test.py 60 5
```
- Duration: 60 seconds
- Concurrent workers: 5

### Option B: Bash Script
```bash
bash load_test.sh 60 5
```

### Option C: Windows Batch
```cmd
load_test.bat 60 5
```

### Option D: Manual Requests
```bash
# Create users
curl -X POST "http://localhost:8000/api/users?name=John&email=john@example.com"
curl -X POST "http://localhost:8000/api/users?name=Jane&email=jane@example.com"

# List users
curl http://localhost:8000/api/users

# Test slow endpoint
curl http://localhost:8000/api/slow

# Test error endpoint
curl http://localhost:8000/api/error
```

## 4️⃣ View Metrics

### Raw Prometheus Format
```bash
curl http://localhost:8000/metrics
```

### Prometheus UI
1. Go to http://localhost:9090
2. Click "Graph" tab
3. Enter query: `rate(http_requests_total[5m])`
4. Click "Execute"

### Grafana Dashboard
1. Go to http://localhost:3000
2. Login with `admin/admin`
3. Click "Dashboards" → "API Monitoring Dashboard"
4. View real-time metrics

## 5️⃣ Explore Dashboards

### Available Panels

1. **Request Rate** - Requests per second over time
2. **Active Requests** - Current in-progress requests
3. **Latency Percentiles** - P50, P95, P99 response times
4. **Error Rate** - Percentage of failed requests
5. **Requests by Status Code** - Distribution of HTTP status codes
6. **Errors by Type** - Error frequency by exception type
7. **Request Distribution** - Traffic by endpoint
8. **Average Response Time** - Latency by endpoint

## 🔍 Common Queries

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

### Active Requests
```promql
http_requests_in_progress
```

## 🛑 Stop the System

```bash
docker-compose down
```

To also remove data:
```bash
docker-compose down -v
```

## 📊 What to Look For

After generating traffic, you should see:

✅ **Prometheus** (http://localhost:9090)
- Targets page shows API as "UP"
- Metrics available in Graph tab

✅ **Grafana** (http://localhost:3000)
- Dashboard shows real-time data
- Graphs update every 10 seconds
- Multiple panels with different metrics

✅ **API** (http://localhost:8000)
- `/metrics` endpoint returns Prometheus format
- `/health` returns healthy status
- CRUD endpoints work correctly

## 🐛 Troubleshooting

### Services won't start
```bash
docker-compose logs
```

### Prometheus can't scrape API
```bash
# Check if API is running
curl http://localhost:8000/health

# Check Prometheus targets
# Visit http://localhost:9090/targets
```

### Grafana shows no data
1. Wait 30 seconds for first scrape
2. Generate traffic with load test
3. Refresh Grafana dashboard

### Port already in use
```bash
# Change ports in docker-compose.yml
# Or stop other services using ports 8000, 9090, 3000
```

## 📚 Next Steps

1. **Explore Prometheus Queries**
   - Visit http://localhost:9090/graph
   - Try different PromQL queries

2. **Customize Grafana Dashboard**
   - Edit panels
   - Add new visualizations
   - Create alerts

3. **Load Test Different Scenarios**
   - Increase concurrent workers
   - Run longer tests
   - Monitor performance

4. **Read Full Documentation**
   - See `README.md` for comprehensive guide
   - Learn about metrics and architecture

## 💡 Tips

- **Refresh Rate**: Grafana dashboard refreshes every 10 seconds
- **Data Retention**: Prometheus keeps 15 days of data
- **Scrape Interval**: Prometheus scrapes every 15 seconds
- **Slow Endpoint**: Takes 2-3 seconds to respond (for testing latency)
- **Error Endpoint**: Always returns 500 error (for testing error tracking)

## 🎯 Success Indicators

You'll know it's working when:

1. ✅ All three services show "Up" in `docker-compose ps`
2. ✅ Prometheus shows API target as "UP"
3. ✅ Grafana dashboard displays graphs with data
4. ✅ Request rate graph shows activity
5. ✅ Error rate graph shows errors from `/api/error` endpoint

---

**Need help?** Check the full README.md for detailed documentation.
