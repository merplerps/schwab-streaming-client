#!/usr/bin/env python3
"""
Setup script for Schwab Streaming Client
This script helps set up the environment and install dependencies
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def setup_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path("schwab_streaming_env")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    # Create virtual environment
    if not run_command("python3 -m venv schwab_streaming_env", "Creating virtual environment"):
        return False
    
    return True


def install_dependencies():
    """Install required dependencies"""
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = "schwab_streaming_env/Scripts/pip"
    else:  # Unix-like systems
        pip_path = "schwab_streaming_env/bin/pip"
    
    # Upgrade pip first
    if not run_command(f"{pip_path} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True


def create_activation_script():
    """Create activation script for easy environment setup"""
    if os.name == 'nt':  # Windows
        activate_script = """@echo off
echo Activating Schwab Streaming Environment...
call schwab_streaming_env\\Scripts\\activate.bat
echo Environment activated! You can now run: python schwab_streaming.py
"""
        script_path = "activate_schwab.bat"
    else:  # Unix-like systems
        activate_script = """#!/bin/bash
echo "Activating Schwab Streaming Environment..."
source schwab_streaming_env/bin/activate
echo "Environment activated! You can now run: python schwab_streaming.py"
"""
        script_path = "activate_schwab.sh"
    
    with open(script_path, 'w') as f:
        f.write(activate_script)
    
    # Make executable on Unix-like systems
    if os.name != 'nt':
        os.chmod(script_path, 0o755)
    
    print(f"✅ Created activation script: {script_path}")
    return True


def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("Please create a .env file with your Schwab API credentials")
        return False
    
    # Read and check .env file
    with open(env_path, 'r') as f:
        content = f.read()
    
    required_vars = ['SCHWAB_API_KEY', 'SCHWAB_APP_SECRET', 'SCHWAB_ACCOUNT_ID']
    missing_vars = []
    
    for var in required_vars:
        if f"{var}=" not in content or f"{var}=your_" in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or incomplete environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with actual credentials")
        return False
    
    print("✅ .env file looks good")
    return True


def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "="*60)
    print("🎉 SCHWAB STREAMING CLIENT SETUP COMPLETE!")
    print("="*60)
    print("\n📋 NEXT STEPS:")
    print("1. Update your .env file with actual Schwab API credentials")
    print("2. Complete OAuth authentication (run the script once to trigger)")
    print("3. Activate the virtual environment:")
    
    if os.name == 'nt':  # Windows
        print("   activate_schwab.bat")
    else:  # Unix-like systems
        print("   source activate_schwab.sh")
    
    print("\n4. Run the streaming client:")
    print("   python schwab_streaming.py [SYMBOLS]")
    print("   Example: python schwab_streaming.py AAPL,GOOGL,MSFT")
    print("\n5. For indefinite streaming, modify the duration in the script")
    
    print("\n📚 USAGE EXAMPLES:")
    print("• Stream default symbols (AAPL, GOOGL, MSFT, TSLA, SPY):")
    print("  python schwab_streaming.py")
    print("\n• Stream custom symbols:")
    print("  python schwab_streaming.py NVDA,AMD,INTC")
    
    print("\n⚠️  IMPORTANT NOTES:")
    print("• Make sure you have valid Schwab API credentials")
    print("• The first run will require OAuth authentication")
    print("• Streaming data is only available during market hours")
    print("• Press Ctrl+C to stop streaming")


def main():
    """Main setup function"""
    print("🚀 SCHWAB STREAMING CLIENT SETUP")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("❌ Failed to setup virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create activation script
    if not create_activation_script():
        print("❌ Failed to create activation script")
        sys.exit(1)
    
    # Check environment file
    env_ok = check_env_file()
    
    # Print usage instructions
    print_usage_instructions()
    
    if not env_ok:
        print("\n⚠️  Remember to update your .env file with actual credentials!")
        sys.exit(1)
    
    print("\n✅ Setup completed successfully!")


if __name__ == "__main__":
    main()
