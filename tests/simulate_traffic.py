import requests
import time
import random
import threading
from datetime import datetime

def simulate_traffic():
    """Simulate realistic traffic patterns to the FastAPI service"""
    base_url = "http://localhost:8000"
    
    # Sample user data for creating users
    sample_users = [
        {"name": "Alice Johnson", "email": "alice@example.com", "age": 28},
        {"name": "Bob Smith", "email": "bob@example.com", "age": 35},
        {"name": "Charlie Brown", "email": "charlie@example.com", "age": 22},
        {"name": "Diana Wilson", "email": "diana@example.com", "age": 31},
        {"name": "Edward Davis", "email": "edward@example.com", "age": 29},
        {"name": "Fiona Miller", "email": "fiona@example.com", "age": 26},
        {"name": "George Taylor", "email": "george@example.com", "age": 33},
        {"name": "Hannah White", "email": "hannah@example.com", "age": 27}
    ]
    
    created_user_ids = []
    
    def make_request(endpoint, method="GET", data=None):
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}")
            elif method == "POST":
                response = requests.post(f"{base_url}{endpoint}", json=data)
            print(f"{datetime.now().strftime('%H:%M:%S')} - {method} {endpoint} - Status: {response.status_code}")
            return response
        except Exception as e:
            print(f"{datetime.now().strftime('%H:%M:%S')} - Error: {e}")
            return None
    
    print("Starting traffic simulation...")
    print("=" * 50)
    
    # Phase 1: Initial setup - create some users
    print("Phase 1: Creating initial users...")
    for i in range(3):
        user_data = random.choice(sample_users)
        response = make_request("/users", "POST", user_data)
        if response and response.status_code == 200:
            user = response.json()
            created_user_ids.append(user['id'])
        time.sleep(1)
    
    # Phase 2: Normal traffic pattern
    print("\nPhase 2: Normal traffic simulation...")
    for i in range(20):
        # Random endpoint selection
        endpoints = [
            ("/", "GET"),
            ("/health", "GET"),
            ("/users", "GET"),
            ("/metrics-info", "GET")
        ]
        
        # Add user-specific endpoints if we have users
        if created_user_ids:
            user_id = random.choice(created_user_ids)
            endpoints.extend([
                (f"/users/{user_id}", "GET"),
            ])
        
        # Occasionally create new users
        if random.random() < 0.3 and len(sample_users) > 0:
            user_data = random.choice(sample_users)
            response = make_request("/users", "POST", user_data)
            if response and response.status_code == 200:
                user = response.json()
                created_user_ids.append(user['id'])
        else:
            endpoint, method = random.choice(endpoints)
            make_request(endpoint, method)
        
        # Random delay between requests (0.5 - 2 seconds)
        time.sleep(random.uniform(0.5, 2.0))
    
    # Phase 3: Error simulation
    print("\nPhase 3: Error scenarios...")
    for i in range(5):
        # Test error endpoint
        make_request("/error", "GET")
        time.sleep(1)
        
        # Test non-existent user
        make_request(f"/users/999{i}", "GET")
        time.sleep(1)
    
    # Phase 4: Load test
    print("\nPhase 4: Load testing...")
    threads = []
    
    def worker():
        for _ in range(10):
            endpoint = random.choice(["/", "/health", "/users"])
            make_request(endpoint, "GET")
            time.sleep(random.uniform(0.1, 0.5))
    
    # Create 5 concurrent threads
    for _ in range(5):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Phase 5: Slow endpoint testing
    print("\nPhase 5: Testing slow endpoints...")
    for i in range(3):
        make_request("/slow", "GET")
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("Traffic simulation completed!")
    print(f"Created {len(created_user_ids)} users during simulation")
    print("Check Grafana dashboards for metrics and logs visualization")

if __name__ == "__main__":
    simulate_traffic()
