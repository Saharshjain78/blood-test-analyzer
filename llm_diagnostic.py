#!/usr/bin/env python3
"""
LLM Diagnostic Script - Test Google Gemini API Connection
"""
import os
from dotenv import load_dotenv
load_dotenv()

def test_google_api_key():
    """Test if Google API key is valid"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ No GOOGLE_API_KEY found in .env file")
        return False
    
    if len(api_key) < 30:
        print(f"❌ API key seems too short: {len(api_key)} characters")
        return False
    
    if not api_key.startswith("AIza"):
        print("❌ Google API key should start with 'AIza'")
        return False
    
    print(f"✅ API key format looks valid: {api_key[:10]}...{api_key[-5:]}")
    return True

def test_langchain_google_genai():
    """Test LangChain Google GenAI integration"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Test with minimal configuration
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.1,
            max_tokens=100,
            max_retries=1
        )
        
        print("✅ ChatGoogleGenerativeAI imported successfully")
        
        # Test a simple call
        response = llm.invoke("Hello, just say 'OK' to confirm you're working")
        print(f"✅ LLM Response: {response.content}")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return False

def test_crewai_agent():
    """Test CrewAI agent with minimal configuration"""
    try:
        from crewai import Agent
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.1,
            max_tokens=100
        )
        
        # Create minimal agent
        test_agent = Agent(
            role="Test Agent",
            goal="Test basic functionality",
            backstory="A simple test agent",
            llm=llm,
            verbose=True,
            max_iter=1,
            max_rpm=10
        )
        
        print("✅ CrewAI Agent created successfully")
        return True
        
    except Exception as e:
        print(f"❌ CrewAI Agent Error: {e}")
        return False

def test_simple_crew():
    """Test a simple crew execution"""
    try:
        from crewai import Agent, Task, Crew, Process
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.1,
            max_tokens=50
        )
        
        # Simple agent
        agent = Agent(
            role="Test",
            goal="Say hello",
            backstory="Test agent",
            llm=llm,
            verbose=False,
            max_iter=1
        )
        
        # Simple task
        task = Task(
            description="Just say 'Hello World'",
            expected_output="The phrase 'Hello World'",
            agent=agent
        )
        
        # Simple crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        print(f"✅ Simple Crew Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Crew Execution Error: {e}")
        return False

def main():
    print("🔍 LLM DIAGNOSTIC TEST")
    print("=" * 50)
    
    tests = [
        ("API Key Validation", test_google_api_key),
        ("LangChain Google GenAI", test_langchain_google_genai),
        ("CrewAI Agent", test_crewai_agent),
        ("Simple Crew Execution", test_simple_crew)
    ]
    
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASS")
            else:
                print(f"❌ {test_name}: FAIL")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! LLM is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
