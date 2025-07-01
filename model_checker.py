#!/usr/bin/env python3
"""
Check available Google Gemini models
"""
import os
from dotenv import load_dotenv
load_dotenv()

def list_available_models():
    """List available Google Gemini models"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        
        print("📋 Available Google Gemini Models:")
        print("-" * 50)
        
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"✅ {model.name}")
                print(f"   Display Name: {model.display_name}")
                print(f"   Description: {model.description}")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False

def test_with_correct_model():
    """Test with the correct model name"""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Try different model names
        model_names = [
            "gemini-1.5-pro",
            "gemini-1.5-flash", 
            "gemini-1.0-pro",
            "models/gemini-pro",
            "models/gemini-1.5-pro"
        ]
        
        for model_name in model_names:
            try:
                print(f"🧪 Testing model: {model_name}")
                
                llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    temperature=0.1,
                    max_tokens=50
                )
                
                response = llm.invoke("Say 'OK' if you can hear me")
                print(f"✅ {model_name} works! Response: {response.content}")
                return model_name
                
            except Exception as e:
                print(f"❌ {model_name} failed: {e}")
                continue
        
        return None
        
    except Exception as e:
        print(f"❌ Error testing models: {e}")
        return None

if __name__ == "__main__":
    print("🔍 GOOGLE GEMINI MODEL CHECKER")
    print("=" * 50)
    
    # First, list available models
    list_available_models()
    
    print("\n" + "=" * 50)
    print("🧪 TESTING DIFFERENT MODEL NAMES")
    print("=" * 50)
    
    # Test with different model names
    working_model = test_with_correct_model()
    
    if working_model:
        print(f"\n🎉 Found working model: {working_model}")
        print("Update your agents.py to use this model name!")
    else:
        print("\n❌ No working model found. Check your API key or try different models.")
