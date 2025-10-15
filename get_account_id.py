#!/usr/bin/env python3
"""
Get Account ID from Schwab API
This script retrieves your Schwab account ID using existing credentials and tokens
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_account_id():
    """Retrieve account ID from Schwab API using existing credentials and tokens"""
    try:
        from schwab.auth import easy_client
        from schwab.client import Client
    except ImportError:
        print("❌ Error: schwab-py library not found")
        print("💡 Please install it using: pip install schwab-py")
        print("💡 Make sure you're in the virtual environment: source schwab_streaming_env/bin/activate")
        return None
    
    # Get credentials from environment
    api_key = os.getenv('SCHWAB_API_KEY')
    app_secret = os.getenv('SCHWAB_APP_SECRET')
    redirect_uri = os.getenv('SCHWAB_REDIRECT_URI', 'https://127.0.0.1:8182')
    token_path = 'schwab_token.json'
    
    # Validate credentials
    if not api_key or api_key.startswith('your_'):
        print("❌ SCHWAB_API_KEY not set or is placeholder")
        print("💡 Please update your .env file with actual API key")
        return None
        
    if not app_secret or app_secret.startswith('your_'):
        print("❌ SCHWAB_APP_SECRET not set or is placeholder")
        print("💡 Please update your .env file with actual app secret")
        return None
    
    # Check if token file exists
    if not os.path.exists(token_path):
        print("❌ No token file found (schwab_token.json)")
        print("💡 You need to complete OAuth authentication first")
        print("💡 Run: python schwab_streaming.py to authenticate")
        print("💡 Or run: python setup_schwab_streaming.py to set up authentication")
        return None
    
    print("✅ Found credentials and token file")
    print(f"📁 Using token file: {os.path.abspath(token_path)}")
    
    try:
        # Create client using existing credentials and token
        print("🔄 Creating Schwab client...")
        client = easy_client(
            api_key=api_key,
            app_secret=app_secret,
            callback_url=redirect_uri,
            token_path=token_path
        )
        print("✅ Client created successfully")
        
        # Get user principals to find account information
        print("🔄 Retrieving account information from Schwab API...")
        principals = client.get_user_principals()
        
        if principals.status_code != 200:
            print(f"❌ Failed to get user principals: {principals.status_code}")
            print(f"Response: {principals.text}")
            return None
        
        principals_data = principals.json()
        accounts = principals_data.get('accounts', [])
        
        if not accounts:
            print("❌ No accounts found in user principals")
            print("💡 Make sure your Schwab account has API access enabled")
            return None
        
        print(f"✅ Found {len(accounts)} account(s):")
        print("=" * 50)
        
        account_ids = []
        for i, account in enumerate(accounts):
            account_id = account.get('accountId', 'Unknown')
            account_type = account.get('type', 'Unknown')
            account_name = account.get('displayName', 'Unknown')
            
            print(f"Account {i+1}:")
            print(f"  ID: {account_id}")
            print(f"  Type: {account_type}")
            print(f"  Name: {account_name}")
            print()
            
            account_ids.append(account_id)
        
        # Return the first account ID (or you can modify this logic)
        selected_account = account_ids[0]
        print(f"🎯 Selected Account ID: {selected_account}")
        
        if len(accounts) > 1:
            print(f"💡 To use a different account, manually set SCHWAB_ACCOUNT_ID in your .env file")
            print(f"💡 Available account IDs: {', '.join(account_ids)}")
        
        return selected_account
        
    except Exception as e:
        print(f"❌ Error retrieving account ID: {e}")
        print("💡 Make sure your API credentials are correct")
        print("💡 Ensure OAuth authentication is complete")
        return None

def update_env_file(account_id):
    """Update the .env file with the retrieved account ID"""
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print("❌ .env file not found")
        return False
    
    try:
        # Read current .env file
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update SCHWAB_ACCOUNT_ID line
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('SCHWAB_ACCOUNT_ID='):
                lines[i] = f'SCHWAB_ACCOUNT_ID={account_id}\n'
                updated = True
                break
        
        # If not found, add it
        if not updated:
            lines.append(f'SCHWAB_ACCOUNT_ID={account_id}\n')
        
        # Write back to file
        with open(env_file, 'w') as f:
            f.writelines(lines)
        
        print(f"✅ Updated .env file with account ID: {account_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def main():
    """Main function"""
    print("🔍 SCHWAB ACCOUNT ID RETRIEVAL")
    print("=" * 40)
    
    # Get account ID
    account_id = get_account_id()
    
    if account_id:
        print("\n" + "=" * 50)
        print("🎉 SUCCESS!")
        print(f"✅ Retrieved Account ID: {account_id}")
        
        # Ask if user wants to update .env file
        try:
            update_env = input("\n💡 Would you like to update your .env file with this account ID? (y/n): ").lower().strip()
            if update_env in ['y', 'yes']:
                if update_env_file(account_id):
                    print("✅ .env file updated successfully!")
                    print("🚀 You can now run: python schwab_streaming.py")
                else:
                    print("❌ Failed to update .env file")
                    print(f"💡 Manually set SCHWAB_ACCOUNT_ID={account_id} in your .env file")
            else:
                print(f"💡 Manually set SCHWAB_ACCOUNT_ID={account_id} in your .env file")
        except KeyboardInterrupt:
            print(f"\n💡 Manually set SCHWAB_ACCOUNT_ID={account_id} in your .env file")
    else:
        print("\n" + "=" * 50)
        print("❌ FAILED TO RETRIEVE ACCOUNT ID")
        print("💡 Check your API credentials and OAuth authentication")
        print("💡 Make sure schwab_token.json exists and is valid")
        sys.exit(1)

if __name__ == "__main__":
    main()
