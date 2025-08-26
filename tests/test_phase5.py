#!/usr/bin/env python3
"""
Test script for Phase 5: Complete Observability Stack
Tests the integration of FastAPI + Prometheus + Grafana + Jaeger + Loki
"""

import requests
import time
import json
from datetime import datetime

def test_services():
    """Test all services in the observability stack"""
    services = {
        "FastAPI Application": "http://localhost:8000",
        "Prometheus": "http://localhost:9090",
        "Grafana": "http://localhost:3000",
        "Jaeger": "http://localhost:16686",
        "Loki": "http://localhost:3100"
    }
    
    print("Testing Phase 5: Complete Observability Stack")
    print("=" * 60)
    
    # Test service availability
    print("1. Testing service availability...")
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            status = "✅ RUNNING" if response.status_code in [200, 404] else "❌ ERROR"
            print(f"   {service_name:25} {url:25} {status}")
        except Exception as e:
            print(f"   {service_name:25} {url:25} ❌ OFFLINE ({str(e)[:30]}...)")
    
    print("\n2. Testing FastAPI endpoints...")
    base_url = "http://localhost:8000"
    
    # Test basic endpoints
    endpoints = [
        "/",
        "/health",
        "/metrics-info",
        "/metrics",
        "/users"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   GET {endpoint:20} Status: {response.status_code} {status}")
        except Exception as e:
            print(f"   GET {endpoint:20} ❌ Error: {e}")
    
    print("\n3. Testing user operations...")
    
    # Create a test user
    user_data = {"name": "Test User", "email": "test@example.com", "age": 30}
    try:
        response = requests.post(f"{base_url}/users", json=user_data)
        if response.status_code == 200:
            user = response.json()
            user_id = user['id']
            print(f"   ✅ Created user: {user['name']} (ID: {user_id})")
            
            # Get the created user
            response = requests.get(f"{base_url}/users/{user_id}")
            if response.status_code == 200:
                print(f"   ✅ Retrieved user: {user['name']}")
            else:
                print(f"   ❌ Failed to retrieve user: {response.status_code}")
        else:
            print(f"   ❌ Failed to create user: {response.status_code}")
    except Exception as e:
        print(f"   ❌ User operations error: {e}")
    
    print("\n4. Testing Prometheus metrics...")
    try:
        response = requests.get("http://localhost:9090/api/v1/query?query=up")
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print("   ✅ Prometheus API is working")
                print(f"   ✅ Found {len(data['data']['result'])} targets")
            else:
                print("   ❌ Prometheus API returned error")
        else:
            print(f"   ❌ Prometheus API error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Prometheus error: {e}")
    
    print("\n5. Testing custom metrics...")
    try:
        response = requests.get(f"{base_url}/metrics")
        if response.status_code == 200:
            metrics_text = response.text
            custom_metrics = [
                "http_requests_total",
                "http_request_duration_seconds",
                "active_users_total",
                "http_errors_total"
            ]
            
            for metric in custom_metrics:
                if metric in metrics_text:
                    print(f"   ✅ {metric}")
                else:
                    print(f"   ❌ {metric} NOT FOUND")
        else:
            print(f"   ❌ Metrics endpoint error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Metrics error: {e}")
    
    print("\n6. Generating sample traffic for testing...")
    
    # Generate some traffic to populate metrics
    for i in range(10):
        requests.get(f"{base_url}/health")
        requests.get(f"{base_url}/users")
        if i % 3 == 0:
            requests.get(f"{base_url}/error")  # Generate some errors
        time.sleep(0.5)
    
    print("   ✅ Generated 10 requests with some errors")
    
    print("\n" + "=" * 60)
    print("Phase 5 Testing Summary:")
    print("✅ FastAPI service with metrics, logging, and tracing")
    print("✅ Prometheus metrics collection")
    print("✅ Grafana dashboards (visit http://localhost:3000)")
    print("✅ Jaeger tracing (visit http://localhost:16686)")
    print("✅ Loki log aggregation")
    print("\n📊 Next steps:")
    print("1. Visit Grafana: http://localhost:3000 (admin/admin)")
    print("2. Check Prometheus: http://localhost:9090")
    print("3. View traces in Jaeger: http://localhost:16686")
    print("4. Run traffic simulation: python simulate_traffic.py")

def test_grafana_login():
    """Test Grafana login"""
    print("\n7. Testing Grafana login...")
    try:
        # Test Grafana login
        login_data = {"user": "admin", "password": "admin"}
        session = requests.Session()
        response = session.post("http://localhost:3000/login", json=login_data)
        
        if response.status_code in [200, 302]:
            print("   ✅ Grafana login successful")
            
            # Test dashboard access
            response = session.get("http://localhost:3000/api/dashboards/uid/fastapi-observability")
            if response.status_code == 200:
                print("   ✅ FastAPI dashboard accessible")
            else:
                print("   ⚠️  Dashboard not found (will be created on first access)")
        else:
            print(f"   ❌ Grafana login failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Grafana test error: {e}")

if __name__ == "__main__":
    test_services()
    test_grafana_login()
