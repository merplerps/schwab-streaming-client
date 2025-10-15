#!/usr/bin/env python3
"""
Simple test script for Schwab Streaming Client
This script tests the basic functionality without requiring OAuth
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_imports():
    """Test if all required modules can be imported"""
    print("🔄 Testing imports...")
    
    try:
        from schwab.auth import easy_client
        from schwab.client import Client
        from schwab.streaming import StreamClient
        print("✅ All schwab-py modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import schwab-py modules: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🔄 Testing environment configuration...")
    
    # Check required environment variables (account_id is now optional)
    required_vars = {
        'SCHWAB_API_KEY': os.getenv('SCHWAB_API_KEY'),
        'SCHWAB_APP_SECRET': os.getenv('SCHWAB_APP_SECRET')
    }
    
    optional_vars = {
        'SCHWAB_ACCOUNT_ID': os.getenv('SCHWAB_ACCOUNT_ID')
    }
    
    missing_vars = []
    for var, value in required_vars.items():
        if not value or value.startswith('your_'):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing or incomplete environment variables: {', '.join(missing_vars)}")
        print("💡 Please update your .env file with actual Schwab API credentials")
        return False
    else:
        print("✅ All required environment variables are set")
        
        # Check optional variables
        missing_optional = []
        for var, value in optional_vars.items():
            if not value or value.startswith('your_'):
                missing_optional.append(var)
        
        if missing_optional:
            print(f"ℹ️  Optional variables not set: {', '.join(missing_optional)}")
            print("💡 Account ID will be retrieved automatically from the API")
        else:
            print("✅ All environment variables are set")
        
        return True

def test_client_creation():
    """Test if we can create the clients without OAuth"""
    print("\n🔄 Testing client creation...")
    
    try:
        from schwab.auth import easy_client
        from schwab.streaming import StreamClient
        
        # Get credentials
        api_key = os.getenv('SCHWAB_API_KEY')
        app_secret = os.getenv('SCHWAB_APP_SECRET')
        account_id = os.getenv('SCHWAB_ACCOUNT_ID')
        redirect_uri = os.getenv('SCHWAB_REDIRECT_URI', 'https://127.0.0.1:8182')
        token_path = 'schwab_token.json'
        
        # Check if token file exists
        if os.path.exists(token_path):
            print("✅ Token file found - attempting to use existing authentication")
            try:
                client = easy_client(
                    api_key=api_key,
                    app_secret=app_secret,
                    callback_url=redirect_uri,
                    token_path=token_path
                )
                stream_client = StreamClient(client, account_id=int(account_id))
                print("✅ Clients created successfully with existing token")
                return True
            except Exception as e:
                print(f"⚠️  Existing token may be invalid: {e}")
                print("💡 You may need to delete schwab_token.json and re-authenticate")
                return False
        else:
            print("ℹ️  No token file found - OAuth authentication required")
            print("💡 Run the main script to complete OAuth authentication")
            return False
            
    except Exception as e:
        print(f"❌ Error creating clients: {e}")
        return False

def show_oauth_instructions():
    """Show OAuth setup instructions"""
    print("\n" + "="*60)
    print("🔐 OAUTH AUTHENTICATION SETUP")
    print("="*60)
    print("To use the Schwab streaming client, you need to complete OAuth authentication:")
    print()
    print("1. 📝 Update your .env file with actual Schwab API credentials")
    print("2. 🌐 Run the main streaming script: python schwab_streaming.py")
    print("3. 🔗 The script will open your browser to Schwab OAuth page")
    print("4. 🔑 Log in to your Schwab account and authorize the application")
    print("5. ✅ The script will automatically capture the authorization code")
    print("6. 🚀 Start streaming real-time market data!")
    print()
    print("📋 OAuth URL Format:")
    print("https://api.schwabapi.com/v1/oauth/authorize?response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%3A8182&client_id=YOUR_CLIENT_ID&scope=readonly&state=market_data")
    print()
    print("💡 Alternative: Try the demo script for mock data:")
    print("   python demo_streaming.py")

def main():
    """Main test function"""
    print("🧪 SCHWAB STREAMING CLIENT - SIMPLE TEST")
    print("="*50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed - check your virtual environment")
        return False
    
    # Test environment
    env_ok = test_environment()
    
    # Test client creation
    client_ok = test_client_creation()
    
    print("\n" + "="*50)
    if env_ok and client_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Ready to stream real-time market data")
        print("\n🚀 Next step: Run 'python schwab_streaming.py' to start streaming")
    elif env_ok:
        print("⚠️  Environment is configured but OAuth authentication needed")
        show_oauth_instructions()
    else:
        print("❌ Configuration issues detected")
        show_oauth_instructions()
    
    return True

if __name__ == "__main__":
    main()
