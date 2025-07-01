#!/usr/bin/env python3
"""
Simple self-test script for Blood Test Analyzer
Run this to quickly verify the system is working
"""
import requests
import os
import time

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ API Health Check: PASS")
            return True
        else:
            print(f"❌ API Health Check: FAIL (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ API Health Check: FAIL (Error: {str(e)})")
        return False

def test_sample_analysis():
    """Test with the sample PDF file"""
    try:
        if not os.path.exists("data/sample.pdf"):
            print("❌ Sample PDF Test: FAIL (sample.pdf not found)")
            return False
            
        with open("data/sample.pdf", "rb") as f:
            files = {"file": ("sample.pdf", f, "application/pdf")}
            data = {"query": "Give me a quick summary of my blood test results"}
            
            print("🔄 Testing sample PDF analysis...")
            start_time = time.time()
            
            response = requests.post(
                "http://localhost:8000/analyze", 
                files=files, 
                data=data, 
                timeout=30
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Sample Analysis: PASS (Completed in {elapsed:.2f}s)")
                print(f"   Analysis length: {len(str(result.get('analysis', '')))} characters")
                return True
            else:
                print(f"❌ Sample Analysis: FAIL (Status: {response.status_code})")
                return False
                
    except Exception as e:
        print(f"❌ Sample Analysis: FAIL (Error: {str(e)})")
        return False

def test_error_handling():
    """Test error handling with invalid file"""
    try:
        files = {"file": ("test.txt", b"Not a PDF", "text/plain")}
        data = {"query": "Test"}
        
        response = requests.post(
            "http://localhost:8000/analyze", 
            files=files, 
            data=data, 
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Error Handling: PASS (Correctly rejects non-PDF files)")
            return True
        else:
            print(f"❌ Error Handling: FAIL (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error Handling: FAIL (Error: {str(e)})")
        return False

def main():
    print("🧪 Blood Test Analyzer - Self Test")
    print("=" * 50)
    
    tests = [
        ("API Health", test_api_health),
        ("Sample Analysis", test_sample_analysis),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name} Test...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
