# Schwab Streaming Client

A Python application that uses the schwab-py library to stream real-time market data from Charles Schwab's API.

## 🚀 Features

- **Real-time Market Data**: Stream live quotes, order book data, and chart information
- **Multiple Data Types**: Support for equity quotes, NASDAQ/NYSE order books, and OHLCV chart data
- **Easy Configuration**: Simple environment-based configuration
- **Automatic Account Detection**: Automatically retrieves your account ID from the Schwab API
- **Flexible Symbol Selection**: Stream data for any valid stock symbols
- **Robust Error Handling**: Comprehensive error handling and logging

## 📋 Prerequisites

- Python 3.8 or higher
- Charles Schwab Developer Account
- Valid Schwab API credentials

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/merplerps/schwab-streaming-client.git
cd schwab-streaming-client
```

### 2. Setup Environment
```bash
python3 setup_schwab_streaming.py
```

### 3. Configure Credentials
Update the `.env` file with your actual Schwab API credentials:

```env
SCHWAB_API_KEY=your_actual_api_key
SCHWAB_APP_SECRET=your_actual_app_secret
SCHWAB_REDIRECT_URI=https://127.0.0.1:8182
# SCHWAB_ACCOUNT_ID=your_actual_account_id  # Optional - auto-retrieved
```

**Note**: The `SCHWAB_ACCOUNT_ID` is now optional! The client will automatically retrieve your account ID from the Schwab API after authentication.

### 4. Activate Environment
```bash
# On macOS/Linux
source activate_schwab.sh

# On Windows
activate_schwab.bat
```

### 5. Run the Streaming Client
```bash
# Stream default symbols (AAPL, GOOGL, MSFT, TSLA, SPY)
python schwab_streaming.py

# Stream custom symbols
python schwab_streaming.py NVDA,AMD,INTC
```

## 🔐 OAuth Authentication

The first time you run the script, you'll need to complete OAuth authentication:

1. The script will open your browser to the Schwab OAuth URL
2. Log in to your Schwab account
3. Authorize the application
4. The script will automatically capture the authorization code
5. A `schwab_token.json` file will be created for future use

## 📊 Data Streams

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

## 🛠️ Configuration

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

## 📚 Usage Examples

### Basic Streaming
```bash
# Stream default symbols for 60 seconds
python schwab_streaming.py

# Stream custom symbols for 60 seconds
python schwab_streaming.py AAPL,GOOGL,MSFT
```

### Account ID Retrieval
```bash
# Automatically get your account ID
python get_account_id.py
```

### Demo Mode (No API Credentials)
```bash
# Try the demo with mock data
python demo_streaming.py
```

## 🧪 Testing

```bash
# Test your configuration
python simple_streaming_test.py

# Test account ID retrieval
python test_account_id_script.py

# Test installation
python test_installation.py
```

## 📁 Project Structure

```
schwab-streaming-client/
├── schwab_streaming.py          # Main streaming client
├── get_account_id.py            # Account ID retrieval script
├── demo_streaming.py            # Demo with mock data
├── setup_schwab_streaming.py    # Setup and installation
├── simple_streaming_test.py     # Configuration testing
├── test_installation.py         # Installation verification
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── activate_schwab.sh           # Environment activation (Linux/Mac)
├── activate_schwab.bat          # Environment activation (Windows)
├── README.md                    # This file
├── README_schwab_streaming.md  # Detailed documentation
├── FIND_ACCOUNT_ID.md          # Account ID lookup guide
├── ACCOUNT_ID_SCRIPT_GUIDE.md  # Account ID script guide
└── ACCOUNT_ID_AUTO_RETRIEVAL.md # Auto-retrieval documentation
```

## 🔧 Troubleshooting

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

## 📋 API Limits

- Schwab API has rate limits for streaming data
- Some data streams may not be available for all symbols
- Market hours restrictions apply to real-time data

## 🔒 Security Notes

- Never commit your `.env` file or `schwab_token.json` to version control
- Keep your API credentials secure
- Use environment variables in production deployments

## 📦 Dependencies

- `schwab-py`: Official Schwab API client
- `python-dotenv`: Environment variable management
- `asyncio`: Asynchronous programming support
- `websockets`: WebSocket communication
- `httpx`: HTTP client library
- `pydantic`: Data validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational and personal use. Please comply with Schwab's API terms of service.

## 🆘 Support

For issues related to:
- **Schwab API**: Contact Schwab Developer Support
- **schwab-py library**: Check the [official documentation](https://schwab-py.readthedocs.io/)
- **This project**: Create an issue in the repository

## 🙏 Acknowledgments

- [schwab-py](https://github.com/alexgolec/schwab-py) - Official Schwab API client
- [Charles Schwab](https://developer.schwab.com/) - API provider
- Python community for excellent libraries

---

**⚠️ Disclaimer**: This software is for educational purposes only. Please ensure compliance with Schwab's API terms of service and applicable regulations.
