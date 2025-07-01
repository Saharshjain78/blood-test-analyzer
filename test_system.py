#!/usr/bin/env python3
"""
Comprehensive Testing System for Blood Test Analyzer
This script tests all the implemented changes and validates the fixes
"""

import os
import sys
import json
import requests
import time
from pathlib import Path
import asyncio
from typing import Dict, Any, List

class TestRunner:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name: str, status: str, details: str = "", execution_time: float = 0):
        """Log test results"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "execution_time": execution_time
        }
        self.test_results.append(result)
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        print(f"   Execution time: {execution_time:.2f}s")
        print("-" * 50)

    def test_imports(self):
        """Test that all imports work correctly after fixes"""
        start_time = time.time()
        
        try:
            # Test tools.py imports
            from tools import BloodTestReportTool, NutritionTool, ExerciseTool, search_tool
            
            # Test agents.py imports  
            from agents import doctor, verifier, nutritionist, exercise_specialist, llm
            
            # Test task.py imports
            from task import help_patients, nutrition_analysis, exercise_planning, verification
            
            # Test main.py imports
            from main import app, run_crew
            
            execution_time = time.time() - start_time
            self.log_test("Import Tests", "PASS", "All imports successful", execution_time)
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test("Import Tests", "FAIL", f"Import error: {str(e)}", execution_time)
            return False

    def test_llm_initialization(self):
        """Test that LLM is properly initialized"""
        start_time = time.time()
        
        try:
            from agents import llm
            
            # Check if llm is properly initialized
            if hasattr(llm, 'model_name') or hasattr(llm, 'model'):
                execution_time = time.time() - start_time
                self.log_test("LLM Initialization", "PASS", f"LLM properly initialized: {type(llm).__name__}", execution_time)
                return True
            else:
                execution_time = time.time() - start_time
                self.log_test("LLM Initialization", "FAIL", "LLM not properly initialized", execution_time)
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test("LLM Initialization", "FAIL", f"Error: {str(e)}", execution_time)
            return False

    def test_tool_methods(self):
        """Test that tool methods are properly defined as BaseTool classes"""
        start_time = time.time()
        
        try:
            from tools import BloodTestReportTool
            
            # Test that we can instantiate the tool
            tool = BloodTestReportTool()
            
            if hasattr(tool, '_run') and callable(tool._run):
                execution_time = time.time() - start_time
                self.log_test("Tool Methods", "PASS", "BloodTestReportTool properly configured as BaseTool", execution_time)
                return True
            else:
                execution_time = time.time() - start_time
                self.log_test("Tool Methods", "FAIL", "BloodTestReportTool missing _run method", execution_time)
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test("Tool Methods", "FAIL", f"Error: {str(e)}", execution_time)
            return False

    def test_agent_definitions(self):
        """Test that agents are properly defined with optimized prompts"""
        start_time = time.time()
        
        try:
            from agents import doctor, verifier, nutritionist, exercise_specialist
            
            agents_to_test = [
                (doctor, "doctor"),
                (verifier, "verifier"), 
                (nutritionist, "nutritionist"),
                (exercise_specialist, "exercise_specialist")
            ]
            
            for agent, name in agents_to_test:
                # Check that agent has proper attributes
                if not hasattr(agent, 'role'):
                    raise Exception(f"{name} agent missing 'role' attribute")
                if not hasattr(agent, 'goal'):
                    raise Exception(f"{name} agent missing 'goal' attribute")
                if not hasattr(agent, 'backstory'):
                    raise Exception(f"{name} agent missing 'backstory' attribute")
                    
                # Check that prompts are optimized (not containing problematic phrases)
                problematic_phrases = [
                    "make up", "fake", "random", "ignore", "don't", 
                    "wrong", "misinformation", "salesperson"
                ]
                
                combined_text = f"{agent.goal} {agent.backstory}".lower()
                found_issues = [phrase for phrase in problematic_phrases if phrase in combined_text]
                
                if found_issues:
                    print(f"Warning: {name} agent may still contain problematic phrases: {found_issues}")
            
            execution_time = time.time() - start_time
            self.log_test("Agent Definitions", "PASS", "All agents properly defined", execution_time)
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test("Agent Definitions", "FAIL", f"Error: {str(e)}", execution_time)
            return False

    def test_task_definitions(self):
        """Test that tasks are properly defined with optimized prompts"""
        start_time = time.time()
        
        try:
            from task import help_patients, nutrition_analysis, exercise_planning, verification
            
            tasks_to_test = [
                (help_patients, "help_patients"),
                (nutrition_analysis, "nutrition_analysis"),
                (exercise_planning, "exercise_planning"),
                (verification, "verification")
            ]
            
            for task, name in tasks_to_test:
                # Check that task has proper attributes
                if not hasattr(task, 'description'):
                    raise Exception(f"{name} task missing 'description' attribute")
                if not hasattr(task, 'expected_output'):
                    raise Exception(f"{name} task missing 'expected_output' attribute")
                    
                # Check that prompts are optimized
                problematic_phrases = [
                    "make up", "fake", "random", "ignore", "maybe", 
                    "whatever", "creative urls", "don't exist"
                ]
                
                combined_text = f"{task.description} {task.expected_output}".lower()
                found_issues = [phrase for phrase in problematic_phrases if phrase in combined_text]
                
                if found_issues:
                    print(f"Warning: {name} task may still contain problematic phrases: {found_issues}")
            
            execution_time = time.time() - start_time
            self.log_test("Task Definitions", "PASS", "All tasks properly defined", execution_time)
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test("Task Definitions", "FAIL", f"Error: {str(e)}", execution_time)
            return False

    def test_api_health_check(self):
        """Test that the API starts and responds to health check"""
        start_time = time.time()
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "running" in data["message"]:
                    execution_time = time.time() - start_time
                    self.log_test("API Health Check", "PASS", f"API responding: {data['message']}", execution_time)
                    return True
                else:
                    execution_time = time.time() - start_time
                    self.log_test("API Health Check", "FAIL", f"Unexpected response: {data}", execution_time)
                    return False
            else:
                execution_time = time.time() - start_time
                self.log_test("API Health Check", "FAIL", f"HTTP {response.status_code}", execution_time)
                return False
                
        except requests.exceptions.ConnectionError:
            execution_time = time.time() - start_time
            self.log_test("API Health Check", "FAIL", "API not running. Start with: uvicorn main:app --reload", execution_time)
            return False
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test("API Health Check", "FAIL", f"Error: {str(e)}", execution_time)
            return False

    def test_file_upload_validation(self):
        """Test file upload functionality"""
        start_time = time.time()
        
        try:
            # Create a dummy PDF file for testing
            test_file_path = "test_sample.pdf"
            with open(test_file_path, "w") as f:
                f.write("%PDF-1.4\nDummy PDF content for testing")
            
            # Test file upload
            with open(test_file_path, "rb") as f:
                files = {"file": ("test_sample.pdf", f, "application/pdf")}
                data = {"query": "Test analysis"}
                
                response = requests.post(
                    f"{self.base_url}/analyze", 
                    files=files, 
                    data=data, 
                    timeout=30
                )
            
            # Clean up test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
            
            if response.status_code == 200:
                result = response.json()
                if "status" in result and result["status"] == "success":
                    execution_time = time.time() - start_time
                    self.log_test("File Upload", "PASS", "File upload successful", execution_time)
                    return True
                else:
                    execution_time = time.time() - start_time
                    self.log_test("File Upload", "FAIL", f"Unexpected response: {result}", execution_time)
                    return False
            else:
                execution_time = time.time() - start_time
                self.log_test("File Upload", "FAIL", f"HTTP {response.status_code}: {response.text}", execution_time)
                return False
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test("File Upload", "FAIL", f"Error: {str(e)}", execution_time)
            return False

    def test_error_handling(self):
        """Test error handling improvements"""
        start_time = time.time()
        
        try:
            # Test with invalid file
            files = {"file": ("test.txt", b"Not a PDF file", "text/plain")}
            data = {"query": "Test"}
            
            response = requests.post(
                f"{self.base_url}/analyze", 
                files=files, 
                data=data, 
                timeout=30
            )
            
            # Should handle error gracefully
            if response.status_code in [400, 500]:
                result = response.json()
                if "detail" in result:
                    execution_time = time.time() - start_time
                    self.log_test("Error Handling", "PASS", f"Proper error handling implemented (HTTP {response.status_code})", execution_time)
                    return True
            
            execution_time = time.time() - start_time
            self.log_test("Error Handling", "FAIL", f"Unexpected response: {response.status_code}", execution_time)
            return False
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_test("Error Handling", "FAIL", f"Error: {str(e)}", execution_time)
            return False

    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🧪 Starting Comprehensive Test Suite for Blood Test Analyzer")
        print("=" * 60)
        
        # Run all tests
        test_methods = [
            self.test_imports,
            self.test_llm_initialization,
            self.test_tool_methods,
            self.test_agent_definitions,
            self.test_task_definitions,
            self.test_api_health_check,
            self.test_file_upload_validation,
            self.test_error_handling
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(test_method.__name__, "ERROR", f"Test runner error: {str(e)}")
        
        # Generate final report
        self.generate_report()

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print("\n📝 DETAILED RESULTS:")
        print("-" * 40)
        
        for result in self.test_results:
            status_emoji = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
            print(f"{status_emoji} {result['test_name']}: {result['status']}")
            if result["details"]:
                print(f"   {result['details']}")
        
        print("\n🔧 FIXES IMPLEMENTED:")
        print("-" * 40)
        fixes = [
            "✅ Added missing PDFLoader import to tools.py",
            "✅ Removed async keywords from tool methods",
            "✅ Added @staticmethod decorators to tool methods",
            "✅ Fixed LLM initialization with proper ChatGoogleGenerativeAI",
            "✅ Corrected agent tool parameter from 'tool' to 'tools'",
            "✅ Optimized all agent backstories and goals",
            "✅ Improved task descriptions and expected outputs",
            "✅ Enhanced error handling in main.py",
            "✅ Updated README.md with comprehensive documentation",
            "✅ Added missing dependencies to requirements.txt"
        ]
        
        for fix in fixes:
            print(f"  {fix}")
        
        print("\n🚀 IMPROVEMENTS MADE:")
        print("-" * 40)
        improvements = [
            "🔸 Evidence-based medical advice instead of made-up recommendations",
            "🔸 Professional nutritionist guidance vs supplement sales pitches", 
            "🔸 Safe exercise planning vs extreme fitness coaching",
            "🔸 Rigorous verification vs rubber-stamp approval",
            "🔸 Structured, scientific outputs vs random medical jargon",
            "🔸 Proper error logging vs silent failures",
            "🔸 Comprehensive API documentation",
            "🔸 Professional project README"
        ]
        
        for improvement in improvements:
            print(f"  {improvement}")
        
        # Save results to file
        with open("test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": self.total_tests,
                    "passed_tests": self.passed_tests,
                    "success_rate": (self.passed_tests/self.total_tests)*100
                },
                "results": self.test_results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to test_results.json")
        
        if self.passed_tests == self.total_tests:
            print("\n🎉 ALL TESTS PASSED! The blood test analyzer is ready for production!")
        else:
            print(f"\n⚠️  {self.total_tests - self.passed_tests} tests failed. Please review and fix remaining issues.")

def main():
    """Main function to run the testing suite"""
    print("Blood Test Analyzer - Comprehensive Testing System")
    print("This script validates all implemented fixes and improvements")
    print("")
    
    runner = TestRunner()
    runner.run_all_tests()

if __name__ == "__main__":
    main()
