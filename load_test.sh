#!/bin/bash

# Load Testing Script for API Monitoring System
# Generates traffic to test metrics collection and visualization

API_URL="http://localhost:8000"
DURATION=${1:-60}  # Default 60 seconds
CONCURRENT=${2:-5} # Default 5 concurrent requests

echo "🚀 Starting load test..."
echo "Duration: ${DURATION}s"
echo "Concurrent requests: ${CONCURRENT}"
echo "Target: ${API_URL}"
echo ""

# Function to make requests
make_requests() {
    local end=$((SECONDS + DURATION))
    
    while [ $SECONDS -lt $end ]; do
        # Create user
        curl -s -X POST "${API_URL}/api/users?name=User$RANDOM&email=user$RANDOM@example.com" > /dev/null &
        
        # List users
        curl -s "${API_URL}/api/users" > /dev/null &
        
        # Get random user
        USER_ID=$((RANDOM % 10 + 1))
        curl -s "${API_URL}/api/users/${USER_ID}" > /dev/null 2>&1 &
        
        # Slow endpoint
        curl -s "${API_URL}/api/slow" > /dev/null &
        
        # Error endpoint (will fail, but that's expected)
        curl -s "${API_URL}/api/error" > /dev/null 2>&1 &
        
        # Health check
        curl -s "${API_URL}/health" > /dev/null &
        
        # Wait a bit before next batch
        sleep 0.5
    done
}

# Run load test
make_requests

echo ""
echo "✅ Load test completed!"
echo ""
echo "📊 View metrics:"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3000 (admin/admin)"
echo "  - Raw metrics: curl http://localhost:8000/metrics"
