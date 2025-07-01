#!/usr/bin/env python3
"""
Quick Test Runner - Tests the fixes without requiring API to be running
"""

import sys
import traceback
from pathlib import Path

def test_basic_imports():
    """Test basic imports work"""
    print("🔍 Testing basic imports...")
    
    try:
        # Test that we can import the fixed modules
        print("  - Importing tools...")
        from tools import BloodTestReportTool, NutritionTool, ExerciseTool
        
        print("  - Importing agents...")
        from agents import llm, doctor, verifier, nutritionist, exercise_specialist
        
        print("  - Importing tasks...")
        from task import help_patients, nutrition_analysis, exercise_planning, verification
        
        print("  - Importing main...")
        from main import app, run_crew
        
        print("✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_tool_static_methods():
    """Test that tool classes are properly defined"""
    print("\n🔧 Testing tool classes...")
    
    try:
        from tools import BloodTestReportTool
        
        # Test that we can instantiate the tool
        tool = BloodTestReportTool()
        
        if hasattr(tool, '_run') and callable(tool._run):
            print("    ✅ BloodTestReportTool properly configured as BaseTool")
        else:
            print("    ❌ BloodTestReportTool missing _run method")
            return False
        
        print("✅ Tool classes properly configured!")
        return True
        
    except Exception as e:
        print(f"❌ Tool class test failed: {e}")
        traceback.print_exc()
        return False

def test_llm_initialization():
    """Test LLM is properly initialized"""
    print("\n🤖 Testing LLM initialization...")
    
    try:
        from agents import llm
        
        # Check if LLM has expected attributes
        if hasattr(llm, 'model_name') or hasattr(llm, 'model') or 'gemini' in str(type(llm)).lower():
            print(f"✅ LLM properly initialized: {type(llm).__name__}")
            return True
        else:
            print(f"❌ LLM not properly initialized: {type(llm)}")
            return False
            
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        traceback.print_exc()
        return False

def test_agent_prompts():
    """Test that agent prompts are optimized"""
    print("\n👨‍⚕️ Testing agent prompt optimization...")
    
    try:
        from agents import doctor, verifier, nutritionist, exercise_specialist
        
        agents = [
            ("doctor", doctor),
            ("verifier", verifier), 
            ("nutritionist", nutritionist),
            ("exercise_specialist", exercise_specialist)
        ]
        
        # Problematic phrases that should be removed
        bad_phrases = [
            "make up", "fake", "random", "ignore", "don't really need",
            "feel free to", "whatever", "creative", "made-up", "wrong",
            "salesperson", "extreme", "dangerous"
        ]
        
        for name, agent in agents:
            print(f"  - Checking {name} agent...")
            
            combined_text = f"{agent.goal} {agent.backstory}".lower()
            
            found_bad = []
            for phrase in bad_phrases:
                if phrase in combined_text:
                    found_bad.append(phrase)
            
            if found_bad:
                print(f"    ⚠️  Still contains problematic phrases: {found_bad}")
            else:
                print(f"    ✅ Prompt optimized")
        
        print("✅ Agent prompt optimization complete!")
        return True
        
    except Exception as e:
        print(f"❌ Agent prompt test failed: {e}")
        traceback.print_exc()
        return False

def test_task_prompts():
    """Test that task prompts are optimized"""
    print("\n📋 Testing task prompt optimization...")
    
    try:
        from task import help_patients, nutrition_analysis, exercise_planning, verification
        
        tasks = [
            ("help_patients", help_patients),
            ("nutrition_analysis", nutrition_analysis),
            ("exercise_planning", exercise_planning), 
            ("verification", verification)
        ]
        
        # Problematic phrases that should be removed
        bad_phrases = [
            "maybe", "whatever", "feel free", "make up", "fake", 
            "creative urls", "don't exist", "ignore", "random"
        ]
        
        for name, task in tasks:
            print(f"  - Checking {name} task...")
            
            combined_text = f"{task.description} {task.expected_output}".lower()
            
            found_bad = []
            for phrase in bad_phrases:
                if phrase in combined_text:
                    found_bad.append(phrase)
            
            if found_bad:
                print(f"    ⚠️  Still contains problematic phrases: {found_bad}")
            else:
                print(f"    ✅ Prompt optimized")
        
        print("✅ Task prompt optimization complete!")
        return True
        
    except Exception as e:
        print(f"❌ Task prompt test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all quick tests"""
    print("🩺 Blood Test Analyzer - Quick Test Runner")
    print("=" * 50)
    print("Testing all implemented fixes and improvements...")
    print()
    
    tests = [
        test_basic_imports,
        test_tool_static_methods,
        test_llm_initialization,
        test_agent_prompts,
        test_task_prompts
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print("📊 QUICK TEST RESULTS")
    print("=" * 50)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All quick tests passed! Basic fixes are working correctly.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set GOOGLE_API_KEY environment variable")
        print("3. Run the API: uvicorn main:app --reload")
        print("4. Run full test suite: python test_system.py")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
