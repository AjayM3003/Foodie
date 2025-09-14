#!/usr/bin/env python3
"""
FoodieBot API Key Management Utility
Easily update API keys and test them
"""

import os
import sys
from dotenv import load_dotenv, set_key

def update_gemini_api_key(new_key):
    """Update Gemini API key in .env file"""
    env_file = '.env'
    
    # Update the .env file
    set_key(env_file, 'GEMINI_API_KEY', new_key)
    print(f"✅ Updated Gemini API key in {env_file}")
    
    # Test the new key
    test_api_key(new_key)

def update_groq_api_key(new_key):
    """Update Groq API key in .env file"""
    env_file = '.env'
    
    # Update the .env file
    set_key(env_file, 'GROQ_API_KEY', new_key)
    print(f"✅ Updated Groq API key in {env_file}")

def test_api_key(api_key):
    """Test if the API key works"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Test with a simple request
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello")
        
        if response.text:
            print("🎉 Gemini API key is working!")
            return True
        else:
            print("❌ Gemini API key test failed - no response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API key test failed: {e}")
        return False

def show_current_status():
    """Show current API key status"""
    load_dotenv()
    
    print("🔍 CURRENT API STATUS")
    print("=" * 40)
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    groq_key = os.getenv('GROQ_API_KEY')
    
    print(f"Gemini API Key: {'Set' if gemini_key else 'Not Set'}")
    if gemini_key:
        print(f"  Preview: {gemini_key[:10]}...{gemini_key[-4:]}")
    
    print(f"Groq API Key: {'Set' if groq_key else 'Not Set'}")
    if groq_key:
        print(f"  Preview: {groq_key[:10]}...{groq_key[-4:]}")
    
    print("\n🧪 Testing APIs...")
    
    # Test Gemini
    if gemini_key:
        test_api_key(gemini_key)
    
    # Test Groq
    if groq_key:
        try:
            from groq import Groq
            client = Groq(api_key=groq_key)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print("🎉 Groq API key is working!")
        except Exception as e:
            print(f"❌ Groq API key test failed: {e}")

def main():
    if len(sys.argv) < 2:
        print("🤖 FoodieBot API Key Manager")
        print("=" * 40)
        print("Usage:")
        print("  python update_api_key.py status              # Show current status")
        print("  python update_api_key.py gemini <new_key>    # Update Gemini key")
        print("  python update_api_key.py groq <new_key>      # Update Groq key")
        print("  python update_api_key.py test                # Test current keys")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'status' or command == 'test':
        show_current_status()
    elif command == 'gemini':
        if len(sys.argv) < 3:
            print("❌ Please provide the new Gemini API key")
            return
        new_key = sys.argv[2]
        update_gemini_api_key(new_key)
    elif command == 'groq':
        if len(sys.argv) < 3:
            print("❌ Please provide the new Groq API key")
            return
        new_key = sys.argv[2]
        update_groq_api_key(new_key)
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
