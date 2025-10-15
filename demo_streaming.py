#!/usr/bin/env python3
"""
Demo script for Schwab Streaming Client
This script demonstrates basic usage without requiring actual API credentials
"""

import asyncio
import json
from datetime import datetime
from typing import List


class MockStreamingClient:
    """Mock streaming client for demonstration purposes"""
    
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
        self.running = False
    
    async def simulate_market_data(self):
        """Simulate real-time market data"""
        print("🚀 Starting Mock Market Data Stream")
        print("=" * 50)
        print(f"📊 Streaming data for: {', '.join(self.symbols)}")
        print("⏱️  Simulating 30 seconds of market data...")
        print("=" * 50)
        
        self.running = True
        start_time = datetime.now()
        
        # Simulate different types of market data
        data_types = [
            "Level One Quote",
            "NASDAQ Order Book",
            "NYSE Order Book", 
            "Chart Data (OHLCV)"
        ]
        
        while self.running:
            elapsed = (datetime.now() - start_time).total_seconds()
            
            if elapsed >= 30:  # Stop after 30 seconds
                break
            
            # Simulate different data types
            for symbol in self.symbols:
                for data_type in data_types:
                    if not self.running:
                        break
                    
                    # Create mock data
                    mock_data = self._create_mock_data(symbol, data_type)
                    
                    # Display the data
                    self._display_data(data_type, mock_data)
                    
                    # Small delay to simulate real-time updates
                    await asyncio.sleep(0.5)
        
        print("\n🏁 Mock streaming session completed")
    
    def _create_mock_data(self, symbol: str, data_type: str) -> dict:
        """Create mock market data"""
        import random
        
        base_price = 100 + hash(symbol) % 200  # Consistent base price per symbol
        variation = random.uniform(-2, 2)
        current_price = base_price + variation
        
        if data_type == "Level One Quote":
            return {
                "key": symbol,
                "1": f"{current_price - 0.1:.2f}",  # Bid
                "2": f"{current_price + 0.1:.2f}",  # Ask
                "3": f"{current_price:.2f}",        # Last
                "4": str(random.randint(1000, 10000)),  # Volume
                "timestamp": int(datetime.now().timestamp() * 1000)
            }
        
        elif data_type == "NASDAQ Order Book":
            return {
                "key": symbol,
                "book_type": "NASDAQ",
                "bids": [
                    {"price": f"{current_price - 0.1:.2f}", "size": random.randint(100, 1000)},
                    {"price": f"{current_price - 0.2:.2f}", "size": random.randint(100, 1000)},
                    {"price": f"{current_price - 0.3:.2f}", "size": random.randint(100, 1000)}
                ],
                "asks": [
                    {"price": f"{current_price + 0.1:.2f}", "size": random.randint(100, 1000)},
                    {"price": f"{current_price + 0.2:.2f}", "size": random.randint(100, 1000)},
                    {"price": f"{current_price + 0.3:.2f}", "size": random.randint(100, 1000)}
                ],
                "timestamp": int(datetime.now().timestamp() * 1000)
            }
        
        elif data_type == "NYSE Order Book":
            return {
                "key": symbol,
                "book_type": "NYSE",
                "bids": [
                    {"price": f"{current_price - 0.05:.2f}", "size": random.randint(100, 1000)},
                    {"price": f"{current_price - 0.15:.2f}", "size": random.randint(100, 1000)},
                    {"price": f"{current_price - 0.25:.2f}", "size": random.randint(100, 1000)}
                ],
                "asks": [
                    {"price": f"{current_price + 0.05:.2f}", "size": random.randint(100, 1000)},
                    {"price": f"{current_price + 0.15:.2f}", "size": random.randint(100, 1000)},
                    {"price": f"{current_price + 0.25:.2f}", "size": random.randint(100, 1000)}
                ],
                "timestamp": int(datetime.now().timestamp() * 1000)
            }
        
        elif data_type == "Chart Data (OHLCV)":
            return {
                "key": symbol,
                "open": f"{current_price - variation:.2f}",
                "high": f"{current_price + abs(variation):.2f}",
                "low": f"{current_price - abs(variation):.2f}",
                "close": f"{current_price:.2f}",
                "volume": str(random.randint(10000, 100000)),
                "timestamp": int(datetime.now().timestamp() * 1000)
            }
        
        return {}
    
    def _display_data(self, data_type: str, data: dict):
        """Display formatted market data"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if data_type == "Level One Quote":
            print(f"\n📈 {data_type} - {timestamp}")
            print(f"   Symbol: {data['key']}")
            print(f"   Bid: ${data['1']} | Ask: ${data['2']} | Last: ${data['3']}")
            print(f"   Volume: {data['4']}")
        
        elif "Order Book" in data_type:
            print(f"\n📊 {data_type} - {timestamp}")
            print(f"   Symbol: {data['key']}")
            print(f"   Bids: {data['bids'][:2]}")  # Show top 2 bids
            print(f"   Asks: {data['asks'][:2]}")  # Show top 2 asks
        
        elif "Chart Data" in data_type:
            print(f"\n📈 {data_type} - {timestamp}")
            print(f"   Symbol: {data['key']}")
            print(f"   OHLC: O=${data['open']} H=${data['high']} L=${data['low']} C=${data['close']}")
            print(f"   Volume: {data['volume']}")


async def main():
    """Main demo function"""
    print("🎭 SCHWAB STREAMING CLIENT - DEMO MODE")
    print("=" * 50)
    print("This is a demonstration of the streaming client")
    print("using mock data. No actual API calls are made.")
    print()
    
    # Demo symbols
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'SPY']
    
    print("📋 DEMO FEATURES:")
    print("• Simulates real-time market data")
    print("• Shows different data types (quotes, order books, charts)")
    print("• Demonstrates the streaming client interface")
    print("• No actual API credentials required")
    print()
    
    # Create and run mock client
    mock_client = MockStreamingClient(symbols)
    
    try:
        await mock_client.simulate_market_data()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
        mock_client.running = False
    
    print("\n" + "=" * 50)
    print("🎯 TO USE WITH REAL DATA:")
    print("1. Get Schwab API credentials")
    print("2. Update .env file with your credentials")
    print("3. Run: python schwab_streaming.py")
    print("4. Complete OAuth authentication")
    print("5. Stream real market data!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Demo ended!")
