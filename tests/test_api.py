import requests
import os

def test_process_claim():
    url = "http://localhost:8000/api/process"
    file_path = "final.pdf" 
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found in root directory.")
        return

    payload = {'claim_id': 'TEST_001'}
    files = [
        ('file', ('final.pdf', open(file_path, 'rb'), 'application/pdf'))
    ]
    
    try:
        response = requests.post(url, data=payload, files=files)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        import json
        print(json.dumps(response.json(), indent=2))
        
        # Save output
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/test_response.json", "w") as f:
            json.dump(response.json(), f, indent=2)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_process_claim()
