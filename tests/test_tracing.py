import requests
import time
import json

def test_tracing():
    base_url = "http://localhost:8000"
    
    print("Testing Phase 4: Distributed Tracing")
    print("=" * 50)
    
    try:
        print("1. Testing basic endpoints to generate traces...")
        
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        print(f"   Root endpoint: {response.status_code}")
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        print(f"   Health endpoint: {response.status_code}")
        
        print("\n2. Creating users to generate detailed traces...")
        
        # Create users with tracing
        users_to_create = [
            {"name": "Alice Johnson", "email": "alice@example.com", "age": 28},
            {"name": "Bob Smith", "email": "bob@example.com", "age": 35},
        ]
        
        created_users = []
        for user_data in users_to_create:
            response = requests.post(f"{base_url}/users", json=user_data)
            if response.status_code == 200:
                user = response.json()
                created_users.append(user)
                print(f"   Created user: {user['name']} (ID: {user['id']})")
            else:
                print(f"   Failed to create user: {user_data['name']} - Status: {response.status_code}")
        
        print("\n3. Testing user retrieval with tracing...")
        
        # Get users with tracing
        for user in created_users:
            response = requests.get(f"{base_url}/users/{user['id']}")
            if response.status_code == 200:
                print(f"   Retrieved user: {user['name']}")
            else:
                print(f"   Failed to retrieve user: {user['name']}")
        
        # Try to get non-existent user (will create error trace)
        response = requests.get(f"{base_url}/users/999")
        print(f"   Non-existent user (999): {response.status_code}")
        
        print("\n4. Testing slow endpoint with detailed tracing...")
        
        # Test slow endpoint (creates interesting trace with child spans)
        start_time = time.time()
        response = requests.get(f"{base_url}/slow")
        end_time = time.time()
        print(f"   Slow endpoint: {response.status_code} (took {end_time - start_time:.2f}s)")
        
        print("\n5. Testing error endpoint to create error traces...")
        
        # Test error endpoint
        response = requests.get(f"{base_url}/error")
        print(f"   Error endpoint: {response.status_code}")
        
        print("\n6. Generating complex trace patterns...")
        
        # Create a more complex trace pattern
        for i in range(2):
            # Get all users
            requests.get(f"{base_url}/users")
            # Create a user
            requests.post(f"{base_url}/users", json={
                "name": f"Trace User {i+1}", 
                "email": f"trace{i+1}@example.com", 
                "age": 25 + i
            })
            # Get health check
            requests.get(f"{base_url}/health")
            time.sleep(0.5)
        
        print("\n✓ Phase 4 tracing testing completed!")
        print("\nTo view traces:")
        print("   - Start Jaeger: docker-compose up jaeger")
        print("   - Open Jaeger UI: http://localhost:16686")
        print("   - Look for service: fastapi-observability-demo")
        print("   - Explore the traces with detailed spans and attributes")
        
    except Exception as e:
        print(f"Error testing service: {e}")

if __name__ == "__main__":
    test_tracing()
