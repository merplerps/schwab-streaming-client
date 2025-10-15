#!/usr/bin/env python3
"""
Schwab Streaming Client for Real-time Market Data
Uses schwab-py library to stream ticker information from Schwab API
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import List, Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    from schwab.auth import easy_client
    from schwab.client import Client
    from schwab.streaming import StreamClient
except ImportError:
    print("Error: schwab-py library not found. Please install it using:")
    print("pip install schwab-py")
    sys.exit(1)


class SchwabStreamingClient:
    """Schwab Streaming Client for real-time market data"""
    
    def __init__(self):
        """Initialize the streaming client with credentials from environment"""
        self.api_key = os.getenv('SCHWAB_API_KEY')
        self.app_secret = os.getenv('SCHWAB_APP_SECRET')
        self.redirect_uri = os.getenv('SCHWAB_REDIRECT_URI', 'https://127.0.0.1:8182')
        self.account_id = os.getenv('SCHWAB_ACCOUNT_ID')  # Optional - will be retrieved from API
        self.token_path = 'schwab_token.json'
        
        # Validate required credentials
        if not all([self.api_key, self.app_secret]):
            raise ValueError(
                "Missing required credentials. Please check your .env file and ensure "
                "SCHWAB_API_KEY and SCHWAB_APP_SECRET are set."
            )
        
        # Account ID is required for now (auto-retrieval can be added later)
        if not self.account_id or self.account_id.startswith('your_'):
            print("⚠️  SCHWAB_ACCOUNT_ID not set or is placeholder")
            print("💡 Please set your actual account ID in the .env file")
            print("💡 You can find your account ID in your Schwab account settings")
            raise ValueError("SCHWAB_ACCOUNT_ID is required. Please set it in your .env file.")
        
        # Initialize clients
        self.client = None
        self.stream_client = None
        
    async def setup_clients(self):
        """Setup HTTP and streaming clients"""
        try:
            # Check if token file exists
            if not os.path.exists(self.token_path):
                print("🔐 No token file found. Starting OAuth authentication...")
                print("📋 Please follow these steps:")
                print("1. The script will open your browser to Schwab OAuth page")
                print("2. Log in to your Schwab account")
                print("3. Authorize the application")
                print("4. The script will automatically capture the authorization code")
                print()
                
                # Create HTTP client with interactive=False to avoid input prompts
                self.client = easy_client(
                    api_key=self.api_key,
                    app_secret=self.app_secret,
                    callback_url=self.redirect_uri,
                    token_path=self.token_path,
                    interactive=False  # Disable interactive mode
                )
            else:
                print("✅ Token file found, using existing authentication")
                # Create HTTP client with existing token
                self.client = easy_client(
                    api_key=self.api_key,
                    app_secret=self.app_secret,
                    callback_url=self.redirect_uri,
                    token_path=self.token_path
                )
            
            # Create streaming client with provided account ID
            self.stream_client = StreamClient(self.client, account_id=int(self.account_id))
            print("✅ Clients initialized successfully")
            
        except Exception as e:
            print(f"❌ Error setting up clients: {e}")
            print("💡 Make sure your API credentials are correct in the .env file")
            print("💡 If this is your first time, you may need to complete OAuth authentication")
            raise
    
    async def get_account_id(self):
        """Retrieve account ID from Schwab API"""
        try:
            print("🔍 Retrieving account information from Schwab API...")
            
            # Get user principals to find account information
            # The easy_client returns a different client type, so we need to use the correct method
            principals = self.client.get_user_principals()
            
            if principals.status_code != 200:
                raise Exception(f"Failed to get user principals: {principals.text}")
            
            principals_data = principals.json()
            
            # Look for accounts in the response
            accounts = principals_data.get('accounts', [])
            
            if not accounts:
                raise Exception("No accounts found in user principals")
            
            # Display available accounts
            print(f"📋 Found {len(accounts)} account(s):")
            for i, account in enumerate(accounts):
                account_id = account.get('accountId', 'Unknown')
                account_type = account.get('type', 'Unknown')
                print(f"   {i+1}. Account ID: {account_id} (Type: {account_type})")
            
            # If only one account, use it automatically
            if len(accounts) == 1:
                account_id = accounts[0].get('accountId')
                print(f"✅ Using single account: {account_id}")
                return account_id
            
            # If multiple accounts, use the first one (you can modify this logic)
            # For now, we'll use the first account, but you could add user selection
            account_id = accounts[0].get('accountId')
            print(f"✅ Using first account: {account_id}")
            print("💡 To use a different account, set SCHWAB_ACCOUNT_ID in your .env file")
            return account_id
            
        except Exception as e:
            print(f"❌ Error retrieving account ID: {e}")
            print("💡 You can manually set SCHWAB_ACCOUNT_ID in your .env file")
            raise
    
    async def login_to_stream(self):
        """Login to the streaming service"""
        try:
            await self.stream_client.login()
            print("✅ Successfully logged into streaming service")
        except Exception as e:
            print(f"❌ Error logging into stream: {e}")
            raise
    
    async def logout_from_stream(self):
        """Logout from the streaming service"""
        try:
            await self.stream_client.logout()
            print("✅ Successfully logged out from streaming service")
        except Exception as e:
            print(f"❌ Error logging out: {e}")
    
    def setup_handlers(self):
        """Setup message handlers for different data streams"""
        
        def print_equity_quote(message):
            """Handler for equity quotes"""
            print(f"\n📈 EQUITY QUOTE - {datetime.now().strftime('%H:%M:%S')}")
            print(json.dumps(message, indent=2))
        
        def print_nasdaq_book(message):
            """Handler for NASDAQ order book data"""
            print(f"\n📊 NASDAQ BOOK - {datetime.now().strftime('%H:%M:%S')}")
            print(json.dumps(message, indent=2))
        
        def print_nyse_book(message):
            """Handler for NYSE order book data"""
            print(f"\n📊 NYSE BOOK - {datetime.now().strftime('%H:%M:%S')}")
            print(json.dumps(message, indent=2))
        
        def print_chart_data(message):
            """Handler for chart/OHLCV data"""
            print(f"\n📈 CHART DATA - {datetime.now().strftime('%H:%M:%S')}")
            print(json.dumps(message, indent=2))
        
        # Register handlers
        self.stream_client.add_level_one_equity_handler(print_equity_quote)
        self.stream_client.add_nasdaq_book_handler(print_nasdaq_book)
        self.stream_client.add_nyse_book_handler(print_nyse_book)
        self.stream_client.add_chart_equity_handler(print_chart_data)
        
        print("✅ Message handlers registered")
    
    async def subscribe_to_symbols(self, symbols: List[str]):
        """Subscribe to streaming data for given symbols"""
        try:
            print(f"🔔 Subscribing to symbols: {', '.join(symbols)}")
            
            # Subscribe to level one equity quotes
            await self.stream_client.level_one_equity_subs(symbols)
            print("✅ Subscribed to equity quotes")
            
            # Subscribe to order books (try both NYSE and NASDAQ)
            try:
                await self.stream_client.nasdaq_book_subs(symbols)
                print("✅ Subscribed to NASDAQ order book")
            except Exception as e:
                print(f"⚠️  Could not subscribe to NASDAQ book: {e}")
            
            try:
                await self.stream_client.nyse_book_subs(symbols)
                print("✅ Subscribed to NYSE order book")
            except Exception as e:
                print(f"⚠️  Could not subscribe to NYSE book: {e}")
            
            # Subscribe to chart data
            try:
                await self.stream_client.chart_equity_subs(symbols)
                print("✅ Subscribed to chart data")
            except Exception as e:
                print(f"⚠️  Could not subscribe to chart data: {e}")
                
        except Exception as e:
            print(f"❌ Error subscribing to symbols: {e}")
            raise
    
    async def stream_data(self, duration_seconds: Optional[int] = None):
        """Stream data for specified duration or indefinitely"""
        print(f"\n🚀 Starting data stream...")
        if duration_seconds:
            print(f"⏱️  Will stream for {duration_seconds} seconds")
        else:
            print("⏱️  Streaming indefinitely (press Ctrl+C to stop)")
        
        start_time = datetime.now()
        
        try:
            while True:
                # Handle incoming messages
                await self.stream_client.handle_message()
                
                # Check if duration limit reached
                if duration_seconds:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    if elapsed >= duration_seconds:
                        print(f"\n⏰ Stream duration of {duration_seconds} seconds completed")
                        break
                        
        except KeyboardInterrupt:
            print("\n🛑 Stream interrupted by user")
        except Exception as e:
            print(f"❌ Error during streaming: {e}")
            raise
    
    async def run_streaming_session(self, symbols: List[str], duration_seconds: Optional[int] = None):
        """Run a complete streaming session"""
        try:
            print("🏁 Starting Schwab Streaming Session")
            print("=" * 50)
            
            # Setup clients
            await self.setup_clients()
            
            # Login to stream
            await self.login_to_stream()
            
            # Setup handlers
            self.setup_handlers()
            
            # Subscribe to symbols
            await self.subscribe_to_symbols(symbols)
            
            # Start streaming
            await self.stream_data(duration_seconds)
            
        except Exception as e:
            print(f"❌ Streaming session failed: {e}")
            raise
        finally:
            # Always try to logout
            try:
                await self.logout_from_stream()
            except:
                pass
            print("🏁 Streaming session ended")


async def main():
    """Main function to run the streaming client"""
    # Default symbols to stream (you can modify this list)
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'SPY']
    
    # Parse command line arguments for custom symbols
    if len(sys.argv) > 1:
        symbols = sys.argv[1].split(',')
        symbols = [s.strip().upper() for s in symbols]
    
    print(f"🎯 Target symbols: {', '.join(symbols)}")
    
    # Create and run streaming client
    streaming_client = SchwabStreamingClient()
    
    # Run for 60 seconds by default (set to None for indefinite streaming)
    duration = 60  # seconds
    
    await streaming_client.run_streaming_session(symbols, duration)


if __name__ == "__main__":
    print("Schwab Streaming Client")
    print("=" * 30)
    print("Make sure you have:")
    print("1. Valid Schwab API credentials in .env file")
    print("2. Completed OAuth authentication")
    print("3. schwab_token.json file with valid tokens")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
