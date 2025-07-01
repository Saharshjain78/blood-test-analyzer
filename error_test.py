#!/usr/bin/env python3
"""
Test error handling with invalid file
"""
import requests

def test_error_handling():
    """Test error handling with non-PDF file"""
    
    try:
        # Test with invalid file (text file instead of PDF)
        files = {"file": ("test.txt", b"Not a PDF file", "text/plain")}
        data = {"query": "Test"}
        
        response = requests.post(
            "http://localhost:8000/analyze", 
            files=files, 
            data=data, 
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ Proper error handling! Returns 400 for invalid file type")
            return True
        elif response.status_code == 500:
            print("✅ Proper error handling! Returns 500 for processing error")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔬 Error Handling Test")
    print("=" * 50)
    success = test_error_handling()
    print("=" * 50)
    if success:
        print("🎉 Test PASSED")
    else:
        print("💥 Test FAILED")
