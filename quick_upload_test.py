#!/usr/bin/env python3
"""
Quick test for file upload optimization
"""
import requests
import os
import time

def test_quick_upload():
    """Test file upload with timeout tracking"""
    
    # Create a simple test PDF
    test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n200\n%%EOF"
    
    test_file_path = "test_upload.pdf"
    with open(test_file_path, "wb") as f:
        f.write(test_content)
    
    try:
        print("🚀 Testing optimized file upload...")
        start_time = time.time()
        
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_blood_report.pdf", f, "application/pdf")}
            data = {"query": "Quick blood test summary"}
            
            response = requests.post(
                "http://localhost:8000/analyze", 
                files=files, 
                data=data, 
                timeout=30
            )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"⏱️  Request completed in {elapsed:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"Status: {result.get('status', 'unknown')}")
            print(f"Query: {result.get('query', 'unknown')}")
            print(f"Analysis length: {len(str(result.get('analysis', '')))}")
            return True
        else:
            print(f"❌ Upload failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"❌ Error after {elapsed:.2f} seconds: {str(e)}")
        return False
        
    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == "__main__":
    print("🔬 Quick Upload Test")
    print("=" * 50)
    success = test_quick_upload()
    print("=" * 50)
    if success:
        print("🎉 Test PASSED")
    else:
        print("💥 Test FAILED")
