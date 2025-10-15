#!/usr/bin/env python3
"""
Test script for the account ID retrieval functionality
This script tests the get_account_id.py script without requiring actual API credentials
"""

import os
import sys
from pathlib import Path

def test_script_exists():
    """Test if the account ID script exists"""
    print("🔄 Testing account ID script...")
    
    script_path = Path("get_account_id.py")
    if script_path.exists():
        print("✅ get_account_id.py script exists")
        return True
    else:
        print("❌ get_account_id.py script not found")
        return False

def test_script_imports():
    """Test if the script can import required modules"""
    print("\n🔄 Testing script imports...")
    
    try:
        # Test if we can import the required modules
        import schwab
        print("✅ schwab-py library available")
    except ImportError:
        print("❌ schwab-py library not found")
        print("💡 Make sure you're in the virtual environment")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv available")
    except ImportError:
        print("❌ python-dotenv not found")
        return False
    
    return True

def test_environment_setup():
    """Test environment configuration"""
    print("\n🔄 Testing environment setup...")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
        
        # Check if it has the required variables
        with open(env_file, 'r') as f:
            content = f.read()
        
        required_vars = ['SCHWAB_API_KEY', 'SCHWAB_APP_SECRET']
        missing_vars = []
        
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=your_" in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing or incomplete variables: {', '.join(missing_vars)}")
            print("💡 Please update your .env file with actual credentials")
            return False
        else:
            print("✅ .env file has required variables")
    else:
        print("❌ .env file not found")
        return False
    
    # Check token file
    token_file = Path("schwab_token.json")
    if token_file.exists():
        print("✅ Token file exists")
        return True
    else:
        print("⚠️  No token file found (schwab_token.json)")
        print("💡 You need to complete OAuth authentication first")
        return False

def show_usage_instructions():
    """Show usage instructions for the account ID script"""
    print("\n" + "="*60)
    print("📋 ACCOUNT ID SCRIPT USAGE")
    print("="*60)
    print("\n🎯 PURPOSE:")
    print("The get_account_id.py script automatically retrieves your Schwab account ID")
    print("using your existing API credentials and authentication tokens.")
    print("\n🚀 USAGE:")
    print("1. Make sure you have valid Schwab API credentials in .env file")
    print("2. Complete OAuth authentication (run schwab_streaming.py once)")
    print("3. Run the account ID script:")
    print("   python get_account_id.py")
    print("\n📋 WHAT IT DOES:")
    print("• Validates your API credentials")
    print("• Uses your existing OAuth token")
    print("• Retrieves all available accounts from Schwab API")
    print("• Displays account information (ID, type, name)")
    print("• Optionally updates your .env file with the account ID")
    print("\n💡 BENEFITS:")
    print("• No manual account ID lookup needed")
    print("• Handles multiple accounts automatically")
    print("• Updates .env file for you")
    print("• Clear error messages and guidance")
    print("\n🔧 TROUBLESHOOTING:")
    print("• Missing credentials: Update .env file with actual API credentials")
    print("• No token file: Complete OAuth authentication first")
    print("• API errors: Check credentials and authentication")
    print("• No accounts: Ensure API access is enabled in Schwab settings")

def main():
    """Main test function"""
    print("🧪 ACCOUNT ID SCRIPT TEST")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test script existence
    if not test_script_exists():
        all_tests_passed = False
    
    # Test imports
    if not test_script_imports():
        all_tests_passed = False
    
    # Test environment
    env_ok = test_environment_setup()
    
    print("\n" + "="*40)
    if all_tests_passed and env_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Account ID script is ready to use")
        print("\n🚀 Next step: Run 'python get_account_id.py' to get your account ID")
    elif all_tests_passed:
        print("⚠️  Script is ready but needs configuration")
        show_usage_instructions()
    else:
        print("❌ Some tests failed")
        show_usage_instructions()
    
    return all_tests_passed

if __name__ == "__main__":
    main()
