import requests
import time

def test_prometheus_metrics():
    base_url = "http://localhost:8000"
    
    print("Testing Phase 2: Prometheus Metrics Integration")
    print("=" * 50)
    
    try:
        # Test basic endpoints
        print("1. Testing basic endpoints...")
        response = requests.get(f"{base_url}/")
        print(f"   Root endpoint: {response.status_code}")
        
        response = requests.get(f"{base_url}/health")
        print(f"   Health endpoint: {response.status_code}")
        
        response = requests.get(f"{base_url}/metrics-info")
        print(f"   Metrics info endpoint: {response.status_code}")
        
        # Test metrics endpoint
        print("\n2. Testing Prometheus metrics endpoint...")
        response = requests.get(f"{base_url}/metrics")
        print(f"   Metrics endpoint: {response.status_code}")
        
        if response.status_code == 200:
            metrics_text = response.text
            print(f"   Metrics length: {len(metrics_text)} characters")
            
            # Check for custom metrics
            custom_metrics = [
                "http_requests_total",
                "http_request_duration_seconds", 
                "active_users_total",
                "http_errors_total"
            ]
            
            print("\n3. Checking for custom metrics...")
            for metric in custom_metrics:
                if metric in metrics_text:
                    print(f"   ✓ {metric} found")
                else:
                    print(f"   ✗ {metric} NOT found")
        
        # Generate some traffic for metrics
        print("\n4. Generating traffic for metrics...")
        for i in range(5):
            requests.get(f"{base_url}/users")
            requests.get(f"{base_url}/health")
            time.sleep(0.5)
        
        # Try to create a user
        user_data = {"name": "Test User", "email": "test@example.com", "age": 25}
        response = requests.post(f"{base_url}/users", json=user_data)
        print(f"   Created user: {response.status_code}")
        
        # Test error endpoint
        response = requests.get(f"{base_url}/error")
        print(f"   Error endpoint: {response.status_code}")
        
        print("\n5. Checking updated metrics...")
        response = requests.get(f"{base_url}/metrics")
        if response.status_code == 200:
            metrics_text = response.text
            # Look for some specific metric values
            lines = metrics_text.split('\n')
            for line in lines:
                if 'http_requests_total' in line and not line.startswith('#'):
                    print(f"   {line}")
                    break
        
        print("\n✓ Phase 2 testing completed successfully!")
        
    except Exception as e:
        print(f"Error testing service: {e}")

if __name__ == "__main__":
    test_prometheus_metrics()
