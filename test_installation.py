#!/usr/bin/env python3
"""
Test script to verify schwab-py installation and basic functionality
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔄 Testing imports...")
    
    try:
        import schwab
        print("✅ schwab-py imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import schwab-py: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        import asyncio
        print("✅ asyncio imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import asyncio: {e}")
        return False
    
    try:
        import websockets
        print("✅ websockets imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import websockets: {e}")
        return False
    
    try:
        import httpx
        print("✅ httpx imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import httpx: {e}")
        return False
    
    try:
        import pydantic
        print("✅ pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pydantic: {e}")
        return False
    
    return True


def test_schwab_modules():
    """Test if specific schwab modules can be imported"""
    print("\n🔄 Testing schwab module imports...")
    
    try:
        from schwab.auth import easy_client
        print("✅ schwab.auth.easy_client imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import schwab.auth.easy_client: {e}")
        return False
    
    try:
        from schwab.client import Client
        print("✅ schwab.client.Client imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import schwab.client.Client: {e}")
        return False
    
    try:
        from schwab.streaming import StreamClient
        print("✅ schwab.streaming.StreamClient imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import schwab.streaming.StreamClient: {e}")
        return False
    
    return True


def test_environment():
    """Test environment setup"""
    print("\n🔄 Testing environment setup...")
    
    # Check if virtual environment exists
    venv_path = Path("schwab_streaming_env")
    if venv_path.exists():
        print("✅ Virtual environment exists")
    else:
        print("❌ Virtual environment not found")
        return False
    
    # Check if .env file exists
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env file exists")
        
        # Check if it has the required variables
        with open(env_path, 'r') as f:
            content = f.read()
        
        required_vars = ['SCHWAB_API_KEY', 'SCHWAB_APP_SECRET', 'SCHWAB_ACCOUNT_ID']
        missing_vars = []
        
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=your_" in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  .env file exists but missing/incomplete variables: {', '.join(missing_vars)}")
            print("   Please update with actual credentials")
        else:
            print("✅ .env file has all required variables")
    else:
        print("❌ .env file not found")
        return False
    
    return True


def test_script_files():
    """Test if required script files exist"""
    print("\n🔄 Testing script files...")
    
    required_files = [
        "schwab_streaming.py",
        "setup_schwab_streaming.py",
        "requirements.txt",
        "README_schwab_streaming.md"
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} not found")
            all_exist = False
    
    return all_exist


def main():
    """Main test function"""
    print("🧪 SCHWAB STREAMING CLIENT - INSTALLATION TEST")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test schwab modules
    if not test_schwab_modules():
        all_tests_passed = False
    
    # Test environment
    if not test_environment():
        all_tests_passed = False
    
    # Test script files
    if not test_script_files():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Installation is complete and ready to use")
        print("\n📋 NEXT STEPS:")
        print("1. Update your .env file with actual Schwab API credentials")
        print("2. Activate the virtual environment: source activate_schwab.sh")
        print("3. Run the streaming client: python schwab_streaming.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the errors above and fix them before proceeding")
        sys.exit(1)


if __name__ == "__main__":
    main()
