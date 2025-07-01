#!/usr/bin/env python3
"""
Setup Script for Blood Test Analyzer
Helps users set up the environment and validate the installation
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("🩺 Blood Test Analyzer - Setup Script")
    print("=" * 50)
    print("This script will help you set up the blood test analyzer system")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_virtual_environment():
    """Check if running in virtual environment"""
    print("\n🏠 Checking virtual environment...")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
        return True
    else:
        print("⚠️  Not running in virtual environment")
        print("   Recommendation: Create a virtual environment:")
        if platform.system() == "Windows":
            print("   python -m venv venv")
            print("   .\\venv\\Scripts\\activate")
        else:
            print("   python -m venv venv")
            print("   source venv/bin/activate")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt file not found")
        return False

def setup_environment_file():
    """Help user set up environment variables"""
    print("\n🔑 Setting up environment variables...")
    
    env_file = Path(".env")
    template_file = Path(".env.template")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if template_file.exists():
        print("📋 Creating .env file from template...")
        try:
            with open(template_file, 'r') as template:
                content = template.read()
            
            with open(env_file, 'w') as env:
                env.write(content)
            
            print("✅ .env file created from template")
            print("⚠️  IMPORTANT: Edit .env file and add your GOOGLE_API_KEY")
            print("   You can get a Google API key from: https://makersuite.google.com/app/apikey")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("⚠️  .env.template not found, creating basic .env file...")
        try:
            with open(env_file, 'w') as env:
                env.write("# Add your Google API Key here\n")
                env.write("GOOGLE_API_KEY=your_google_api_key_here\n")
            
            print("✅ Basic .env file created")
            print("⚠️  IMPORTANT: Edit .env file and add your GOOGLE_API_KEY")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False

def run_quick_tests():
    """Run quick validation tests"""
    print("\n🧪 Running quick validation tests...")
    
    try:
        result = subprocess.run([sys.executable, "quick_test.py"], 
                               capture_output=True, text=True, timeout=30)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print("✅ Quick tests passed!")
            return True
        else:
            print("❌ Some quick tests failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out - this might indicate missing dependencies")
        return False
    except FileNotFoundError:
        print("⚠️  quick_test.py not found - skipping tests")
        return True
    except Exception as e:
        print(f"⚠️  Test error: {e}")
        return True  # Don't fail setup for test issues

def print_next_steps():
    """Print next steps for the user"""
    print("\n🚀 Next Steps:")
    print("=" * 30)
    print("1. Edit .env file and add your GOOGLE_API_KEY")
    print("   - Get key from: https://makersuite.google.com/app/apikey")
    print("   - Replace 'your_google_api_key_here' with your actual key")
    print()
    print("2. Start the application:")
    print("   uvicorn main:app --reload")
    print()
    print("3. Test the API:")
    print("   - Open http://localhost:8000 in your browser")
    print("   - Use the /analyze endpoint to upload blood test PDFs")
    print()
    print("4. Run comprehensive tests:")
    print("   python test_system.py")
    print()
    print("5. View API documentation:")
    print("   http://localhost:8000/docs")

def main():
    """Main setup function"""
    print_header()
    
    # Run all setup steps
    steps = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Environment Variables", setup_environment_file),
        ("Quick Tests", run_quick_tests)
    ]
    
    results = []
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"❌ {step_name} failed with error: {e}")
            results.append((step_name, False))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Setup Summary")
    print("=" * 50)
    
    for step_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{step_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        print(f"\n🎉 Setup completed successfully! ({passed}/{total})")
    else:
        print(f"\n⚠️  Setup completed with issues ({passed}/{total})")
        print("Please review the failed steps above")
    
    print_next_steps()

if __name__ == "__main__":
    main()
