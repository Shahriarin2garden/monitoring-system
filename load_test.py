#!/usr/bin/env python3
"""
Load Testing Script for API Monitoring System
Generates traffic to test metrics collection and visualization
"""

import requests
import time
import random
import threading
import sys
from datetime import datetime

API_URL = "http://localhost:8000"
DURATION = 60  # seconds
CONCURRENT = 5  # concurrent threads

def log(message):
    """Print timestamped message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def make_request(method, endpoint, **kwargs):
    """Make HTTP request safely"""
    try:
        url = f"{API_URL}{endpoint}"
        if method == "GET":
            requests.get(url, timeout=5, **kwargs)
        elif method == "POST":
            requests.post(url, timeout=5, **kwargs)
        elif method == "PUT":
            requests.put(url, timeout=5, **kwargs)
        elif method == "DELETE":
            requests.delete(url, timeout=5, **kwargs)
    except Exception as e:
        pass  # Silently ignore errors (expected for /api/error)

def worker(worker_id, duration):
    """Worker thread that makes requests"""
    end_time = time.time() + duration
    request_count = 0
    
    while time.time() < end_time:
        try:
            # Create user
            user_id = random.randint(1, 1000)
            make_request("POST", f"/api/users?name=User{user_id}&email=user{user_id}@example.com")
            request_count += 1
            
            # List users
            make_request("GET", "/api/users")
            request_count += 1
            
            # Get random user
            user_id = random.randint(1, 10)
            make_request("GET", f"/api/users/{user_id}")
            request_count += 1
            
            # Slow endpoint
            make_request("GET", "/api/slow")
            request_count += 1
            
            # Error endpoint
            make_request("GET", "/api/error")
            request_count += 1
            
            # Health check
            make_request("GET", "/health")
            request_count += 1
            
            # Small delay between request batches
            time.sleep(0.1)
            
        except Exception as e:
            pass
    
    log(f"Worker {worker_id} completed: {request_count} requests")

def main():
    """Main load test function"""
    global DURATION, CONCURRENT
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            DURATION = int(sys.argv[1])
        except ValueError:
            print("Invalid duration. Using default 60 seconds.")
    
    if len(sys.argv) > 2:
        try:
            CONCURRENT = int(sys.argv[2])
        except ValueError:
            print("Invalid concurrent count. Using default 5.")
    
    print("\n" + "="*50)
    print("  API Monitoring System - Load Test")
    print("="*50)
    print(f"\nDuration: {DURATION} seconds")
    print(f"Concurrent workers: {CONCURRENT}")
    print(f"Target: {API_URL}")
    print("\nStarting load test...\n")
    
    # Create and start worker threads
    threads = []
    start_time = time.time()
    
    for i in range(CONCURRENT):
        thread = threading.Thread(target=worker, args=(i+1, DURATION))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        log(f"Started worker {i+1}")
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*50)
    print("  Load Test Completed!")
    print("="*50)
    print(f"\nElapsed time: {elapsed:.2f} seconds")
    print(f"Workers: {CONCURRENT}")
    print("\nView metrics:")
    print("  - Prometheus: http://localhost:9090")
    print("  - Grafana: http://localhost:3000 (admin/admin)")
    print("  - Raw metrics: curl http://localhost:8000/metrics")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nLoad test interrupted by user.")
        sys.exit(0)
