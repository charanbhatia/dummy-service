import requests
import time
import json

def test_logging():
    base_url = "http://localhost:8000"
    
    print("Testing Phase 3: Structured Logging")
    print("=" * 50)
    
    try:
        print("1. Testing basic endpoints with logging...")
        
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        print(f"   Root endpoint: {response.status_code}")
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        print(f"   Health endpoint: {response.status_code}")
        
        print("\n2. Creating users to generate logs...")
        
        # Create some users
        users_to_create = [
            {"name": "Alice Johnson", "email": "alice@example.com", "age": 28},
            {"name": "Bob Smith", "email": "bob@example.com", "age": 35},
            {"name": "Charlie Brown", "email": "charlie@example.com", "age": 22}
        ]
        
        created_users = []
        for user_data in users_to_create:
            response = requests.post(f"{base_url}/users", json=user_data)
            if response.status_code == 201:
                user = response.json()
                created_users.append(user)
                print(f"   Created user: {user['name']} (ID: {user['id']})")
            else:
                print(f"   Failed to create user: {user_data['name']}")
        
        print("\n3. Testing user retrieval...")
        
        # Get users
        for user in created_users:
            response = requests.get(f"{base_url}/users/{user['id']}")
            if response.status_code == 200:
                print(f"   Retrieved user: {user['name']}")
            else:
                print(f"   Failed to retrieve user: {user['name']}")
        
        # Try to get non-existent user
        response = requests.get(f"{base_url}/users/999")
        print(f"   Non-existent user (999): {response.status_code}")
        
        print("\n4. Testing error scenarios...")
        
        # Test error endpoint
        response = requests.get(f"{base_url}/error")
        print(f"   Error endpoint: {response.status_code}")
        
        print("\n5. Testing slow endpoint...")
        
        # Test slow endpoint
        start_time = time.time()
        response = requests.get(f"{base_url}/slow")
        end_time = time.time()
        print(f"   Slow endpoint: {response.status_code} (took {end_time - start_time:.2f}s)")
        
        print("\n6. Generating multiple requests for logging...")
        
        # Generate some traffic
        for i in range(3):
            requests.get(f"{base_url}/users")
            requests.get(f"{base_url}/health")
            time.sleep(0.5)
        
        print("\n✓ Phase 3 logging testing completed!")
        print("\nCheck the following for logs:")
        print("   - Console output (structured JSON logs)")
        print("   - logs/app.log file (if running locally)")
        
    except Exception as e:
        print(f"Error testing service: {e}")

if __name__ == "__main__":
    test_logging()
