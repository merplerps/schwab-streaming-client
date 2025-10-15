#!/usr/bin/env python3
"""
Test script to verify account ID retrieval from Schwab API
This script tests the account ID retrieval functionality
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_account_retrieval():
    """Test account ID retrieval from Schwab API"""
    print("🧪 TESTING ACCOUNT ID RETRIEVAL")
    print("=" * 40)
    
    try:
        from schwab.auth import easy_client
        from schwab.client import Client
        
        # Get credentials
        api_key = os.getenv('SCHWAB_API_KEY')
        app_secret = os.getenv('SCHWAB_APP_SECRET')
        redirect_uri = os.getenv('SCHWAB_REDIRECT_URI', 'https://127.0.0.1:8182')
        token_path = 'schwab_token.json'
        
        # Check if we have credentials
        if not api_key or api_key.startswith('your_'):
            print("❌ SCHWAB_API_KEY not set or is placeholder")
            print("💡 Please update your .env file with actual API key")
            return False
            
        if not app_secret or app_secret.startswith('your_'):
            print("❌ SCHWAB_APP_SECRET not set or is placeholder")
            print("💡 Please update your .env file with actual app secret")
            return False
        
        print("✅ API credentials found")
        
        # Check if token file exists
        if not os.path.exists(token_path):
            print("❌ No token file found (schwab_token.json)")
            print("💡 You need to complete OAuth authentication first")
            print("💡 Run: python schwab_streaming.py to authenticate")
            return False
        
        print("✅ Token file found")
        
        # Create client
        print("🔄 Creating Schwab client...")
        client = easy_client(
            api_key=api_key,
            app_secret=app_secret,
            callback_url=redirect_uri,
            token_path=token_path
        )
        print("✅ Client created successfully")
        
        # Test account retrieval
        print("🔄 Retrieving account information...")
        principals = client.get_user_principals()
        
        if principals.status_code != 200:
            print(f"❌ Failed to get user principals: {principals.status_code}")
            print(f"Response: {principals.text}")
            return False
        
        principals_data = principals.json()
        accounts = principals_data.get('accounts', [])
        
        if not accounts:
            print("❌ No accounts found in user principals")
            return False
        
        print(f"✅ Found {len(accounts)} account(s):")
        for i, account in enumerate(accounts):
            account_id = account.get('accountId', 'Unknown')
            account_type = account.get('type', 'Unknown')
            print(f"   {i+1}. Account ID: {account_id} (Type: {account_type})")
        
        # Test account selection logic
        if len(accounts) == 1:
            selected_account = accounts[0].get('accountId')
            print(f"✅ Single account detected: {selected_account}")
        else:
            selected_account = accounts[0].get('accountId')
            print(f"✅ Multiple accounts detected, using first: {selected_account}")
            print("💡 To use a different account, set SCHWAB_ACCOUNT_ID in your .env file")
        
        print("\n🎉 Account ID retrieval test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the virtual environment: source schwab_streaming_env/bin/activate")
        return False
    except Exception as e:
        print(f"❌ Error during account retrieval: {e}")
        return False

async def main():
    """Main test function"""
    success = await test_account_retrieval()
    
    if success:
        print("\n" + "="*50)
        print("🎉 ACCOUNT ID RETRIEVAL WORKING!")
        print("✅ The streaming client will automatically get your account ID")
        print("✅ No need to manually set SCHWAB_ACCOUNT_ID in .env file")
        print("\n🚀 Ready to run: python schwab_streaming.py")
    else:
        print("\n" + "="*50)
        print("❌ ACCOUNT ID RETRIEVAL FAILED")
        print("💡 Check your API credentials and OAuth authentication")
        print("💡 Make sure schwab_token.json exists and is valid")

if __name__ == "__main__":
    asyncio.run(main())
