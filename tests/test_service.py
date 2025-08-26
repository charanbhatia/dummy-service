import requests
import json

def test_service():
    base_url = "http://localhost:8000"
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        print("Root endpoint:", response.json())
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        print("Health endpoint:", response.json())
        
        # Test users endpoint
        response = requests.get(f"{base_url}/users")
        print("Users endpoint:", response.json())
        
        print("All tests passed!")
        
    except Exception as e:
        print(f"Error testing service: {e}")

if __name__ == "__main__":
    test_service()
