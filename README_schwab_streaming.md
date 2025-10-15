# Schwab Streaming Client

A Python application that uses the schwab-py library to stream real-time market data from Charles Schwab's API.

## Features

- **Real-time Market Data**: Stream live quotes, order book data, and chart information
- **Multiple Data Types**: Support for equity quotes, NASDAQ/NYSE order books, and OHLCV chart data
- **Easy Configuration**: Simple environment-based configuration
- **Automatic Account Detection**: Automatically retrieves your account ID from the Schwab API
- **Flexible Symbol Selection**: Stream data for any valid stock symbols
- **Robust Error Handling**: Comprehensive error handling and logging

## Prerequisites

- Python 3.8 or higher
- Charles Schwab Developer Account
- Valid Schwab API credentials

## Quick Start

### 1. Setup Environment

Run the setup script to create the virtual environment and install dependencies:

```bash
python3 setup_schwab_streaming.py
```

### 2. Configure Credentials

Update the `.env` file with your actual Schwab API credentials:

```env
SCHWAB_API_KEY=your_actual_api_key
SCHWAB_APP_SECRET=your_actual_app_secret
SCHWAB_REDIRECT_URI=https://127.0.0.1:8182
# SCHWAB_ACCOUNT_ID=your_actual_account_id  # Optional - auto-retrieved
```

**Note**: The `SCHWAB_ACCOUNT_ID` is now optional! The client will automatically retrieve your account ID from the Schwab API after authentication. If you have multiple accounts, it will use the first one, or you can manually specify which account to use.

### 3. Activate Environment

**On macOS/Linux:**
```bash
source activate_schwab.sh
```

**On Windows:**
```cmd
activate_schwab.bat
```

### 4. Run the Streaming Client

**Stream default symbols (AAPL, GOOGL, MSFT, TSLA, SPY):**
```bash
python schwab_streaming.py
```

**Stream custom symbols:**
```bash
python schwab_streaming.py NVDA,AMD,INTC
```

## OAuth Authentication

The first time you run the script, you'll need to complete OAuth authentication:

1. The script will open your browser to the Schwab OAuth URL
2. Log in to your Schwab account
3. Authorize the application
4. The script will automatically capture the authorization code
5. A `schwab_token.json` file will be created for future use

## Data Streams

The client supports multiple types of real-time data:

### Level One Quotes
- Real-time bid/ask prices
- Last trade information
- Volume and timestamp data

### Order Book Data
- NASDAQ Level 2 order book
- NYSE Level 2 order book
- Bid/ask depth information

### Chart Data (OHLCV)
- Open, High, Low, Close prices
- Volume data
- Time-based intervals

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SCHWAB_API_KEY` | Your Schwab API key | Yes |
| `SCHWAB_APP_SECRET` | Your Schwab app secret | Yes |
| `SCHWAB_ACCOUNT_ID` | Your Schwab account ID | No (auto-retrieved) |
| `SCHWAB_REDIRECT_URI` | OAuth redirect URI | No (default: https://127.0.0.1:8182) |

### Script Configuration

You can modify the streaming behavior in `schwab_streaming.py`:

- **Default symbols**: Change the `symbols` list in the `main()` function
- **Stream duration**: Modify the `duration` variable (set to `None` for indefinite streaming)
- **Data handlers**: Customize the message handlers for different data types

## Usage Examples

### Basic Streaming
```bash
# Stream default symbols for 60 seconds
python schwab_streaming.py

# Stream custom symbols for 60 seconds
python schwab_streaming.py AAPL,GOOGL,MSFT
```

### Market Hours Streaming
```python
# Modify the script to stream during market hours
# Set duration to None for indefinite streaming
duration = None  # Stream indefinitely
```

### Custom Data Handling
```python
def custom_quote_handler(message):
    """Custom handler for equity quotes"""
    symbol = message.get('key', 'UNKNOWN')
    bid = message.get('1', 'N/A')
    ask = message.get('2', 'N/A')
    print(f"{symbol}: Bid=${bid}, Ask=${ask}")

# Register custom handler
stream_client.add_level_one_equity_handler(custom_quote_handler)
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure your API credentials are correct
   - Check that the OAuth redirect URI matches your app configuration
   - Delete `schwab_token.json` and re-authenticate if needed

2. **No Data Received**
   - Verify you're running during market hours
   - Check that the symbols are valid and tradeable
   - Ensure your account has streaming data permissions

3. **Connection Errors**
   - Check your internet connection
   - Verify Schwab API service status
   - Try restarting the application

### Debug Mode

Enable debug logging by modifying the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## API Limits

- Schwab API has rate limits for streaming data
- Some data streams may not be available for all symbols
- Market hours restrictions apply to real-time data

## Security Notes

- Never commit your `.env` file or `schwab_token.json` to version control
- Keep your API credentials secure
- Use environment variables in production deployments

## Dependencies

- `schwab-py`: Official Schwab API client
- `python-dotenv`: Environment variable management
- `asyncio`: Asynchronous programming support
- `websockets`: WebSocket communication
- `httpx`: HTTP client library
- `pydantic`: Data validation

## License

This project is for educational and personal use. Please comply with Schwab's API terms of service.

## Support

For issues related to:
- **Schwab API**: Contact Schwab Developer Support
- **schwab-py library**: Check the [official documentation](https://schwab-py.readthedocs.io/)
- **This script**: Create an issue in the repository

## Contributing

Feel free to submit issues and enhancement requests!
