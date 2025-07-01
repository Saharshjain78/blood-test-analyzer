import requests

# Replace 'your_file.pdf' with path to your PDF
with open("data/sample.pdf", "rb") as f:
    files = {"file": ("my_test.pdf", f, "application/pdf")}
    data = {"query": "What are the key findings in this blood test?"}
    
    response = requests.post("http://localhost:8000/analyze", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Success!")
        print(f"Analysis: {result['analysis']}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
