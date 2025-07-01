# 🧪 Manual Testing Guide for Blood Test Analyzer

## Prerequisites

⚠️ **IMPORTANT: Check Server Status First**
```bash
# Always check if server is already running before starting
python -c "import requests; print('API Status:', requests.get('http://localhost:8000/').status_code)" 2>nul || echo "Server not running - need to start"
```

1. **If server is not running**, start it:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. Verify your .env file contains your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Testing Methods

### Method 1: Command Line Testing
```bash
# Run the self-test script
python self_test.py

# Run the comprehensive test suite
python test_system.py

# Run the quick test
python quick_test.py
```

### Method 2: Browser Testing
1. Open your browser and go to: `http://localhost:8000/`
2. You should see: `{"message":"Blood Test Report Analyser API is running"}`

### Method 3: API Testing with curl (if available)
```bash
# Test health endpoint
curl http://localhost:8000/

# Test file upload (replace with your PDF file)
curl -X POST "http://localhost:8000/analyze" \
     -F "file=@data/sample.pdf" \
     -F "query=Analyze my blood test"
```

### Method 4: Python Interactive Testing
```python
import requests

# Test health
response = requests.get("http://localhost:8000/")
print(response.json())

# Test file upload
with open("data/sample.pdf", "rb") as f:
    files = {"file": ("test.pdf", f, "application/pdf")}
    data = {"query": "Summarize my blood test"}
    response = requests.post("http://localhost:8000/analyze", files=files, data=data)
    print(response.json())
```

## What to Expect

### ✅ Successful Test Results:
- **API Health**: Returns `{"message":"Blood Test Report Analyser API is running"}`
- **File Upload**: Returns JSON with status "success" and analysis text
- **Error Handling**: Invalid files return HTTP 400 with error message
- **Processing Time**: Analysis completes in 2-5 seconds

### ❌ Common Issues:
- **Connection Refused**: API server not running - start with `python main.py`
- **Import Errors**: Dependencies missing - run `pip install -r requirements.txt`
- **API Key Error**: Missing/invalid Google API key in .env file
- **Timeout**: Large files or complex queries may take longer

## Sample Test Cases

### Test Case 1: Valid PDF Analysis
- **Input**: Upload `data/sample.pdf` with query "Summarize my results"
- **Expected**: JSON response with analysis text and status "success"

### Test Case 2: Invalid File Type
- **Input**: Upload a .txt file instead of PDF
- **Expected**: HTTP 400 error with message about PDF requirement

### Test Case 3: Empty Query
- **Input**: Upload PDF with empty query
- **Expected**: Uses default query "Summarise my Blood Test Report"

### Test Case 4: Large File
- **Input**: Upload a large PDF (>5MB)
- **Expected**: Should process successfully but may take longer

## Troubleshooting

### Port Already in Use Error (Error 10048)
If you see: `[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000):`

**Solution 1: Check if server is already running**
```bash
# Test if API is already running
python -c "import requests; print('API Status:', requests.get('http://localhost:8000/').status_code)"
```

**Solution 2: Find and stop the existing process**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID_NUMBER> /F
```

**Solution 3: Use a different port**
```bash
# Start server on port 8001 instead
python -m uvicorn main:app --host 0.0.0.0 --port 8001

# Then test with:
python -c "import requests; print('API Status:', requests.get('http://localhost:8001/').status_code)"
```

**Solution 4: Check if server is already working**
Since you're getting this error, the API might already be running successfully on port 8000. Try testing it first before starting another instance.

### Server Won't Start
```bash
# Check if port 8000 is in use
netstat -an | findstr :8000

# Try different port
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python environment
python --version
pip list
```

### API Key Issues
1. Check .env file exists and contains GOOGLE_API_KEY
2. Verify API key is valid and has Gemini Pro access
3. Check for extra spaces or quotes around the key

## Performance Benchmarks
- **API Health Check**: < 100ms
- **File Upload & Analysis**: 2-5 seconds
- **Error Response**: < 100ms
- **Memory Usage**: < 500MB during processing
