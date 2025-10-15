# Account ID Retrieval Script Guide

## 🎯 Purpose

The `get_account_id.py` script automatically retrieves your Schwab account ID using your existing API credentials and authentication tokens.

## 🚀 Quick Start

### Prerequisites
1. ✅ Schwab API credentials set in `.env` file
2. ✅ OAuth authentication completed (token file exists)
3. ✅ Virtual environment activated

### Run the Script
```bash
# Activate virtual environment
source schwab_streaming_env/bin/activate

# Run the account ID retrieval script
python get_account_id.py
```

## 📋 What the Script Does

1. **Validates Credentials**: Checks your `.env` file for valid API credentials
2. **Checks Authentication**: Verifies that OAuth token file exists
3. **Creates API Client**: Uses your credentials and existing token
4. **Retrieves Account Info**: Calls Schwab API to get account information
5. **Displays Results**: Shows all available accounts with details
6. **Updates .env File**: Optionally updates your `.env` file with the account ID

## 🔧 Script Features

### Automatic Account Detection
- Finds all accounts associated with your Schwab account
- Displays account ID, type, and name for each account
- Automatically selects the first account (or you can choose)

### Smart .env File Updates
- Optionally updates your `.env` file with the retrieved account ID
- Preserves existing configuration
- Adds account ID if not present

### Comprehensive Error Handling
- Clear error messages for missing credentials
- Guidance for OAuth authentication issues
- Helpful troubleshooting tips

## 📊 Example Output

```
🔍 SCHWAB ACCOUNT ID RETRIEVAL
========================================
✅ Found credentials and token file
📁 Using token file: /path/to/schwab_token.json
🔄 Creating Schwab client...
✅ Client created successfully
🔄 Retrieving account information from Schwab API...
✅ Found 2 account(s):
==================================================
Account 1:
  ID: 123456789
  Type: CASH
  Name: Individual Account

Account 2:
  ID: 987654321
  Type: MARGIN
  Name: Margin Account

🎯 Selected Account ID: 123456789

💡 Would you like to update your .env file with this account ID? (y/n): y
✅ Updated .env file with account ID: 123456789
✅ .env file updated successfully!
🚀 You can now run: python schwab_streaming.py
```

## 🛠️ Troubleshooting

### Missing Credentials
```
❌ SCHWAB_API_KEY not set or is placeholder
💡 Please update your .env file with actual API key
```
**Solution**: Update your `.env` file with actual Schwab API credentials

### No Token File
```
❌ No token file found (schwab_token.json)
💡 You need to complete OAuth authentication first
```
**Solution**: Run `python schwab_streaming.py` to complete OAuth authentication

### API Errors
```
❌ Failed to get user principals: 401
```
**Solution**: Check your API credentials and ensure OAuth authentication is complete

### No Accounts Found
```
❌ No accounts found in user principals
💡 Make sure your Schwab account has API access enabled
```
**Solution**: Ensure your Schwab account has API access enabled in your developer settings

## 🔄 Workflow Integration

### Complete Setup Workflow
```bash
# 1. Set up environment
python setup_schwab_streaming.py

# 2. Update .env with API credentials
nano .env

# 3. Complete OAuth authentication
python schwab_streaming.py

# 4. Get account ID automatically
python get_account_id.py

# 5. Start streaming
python schwab_streaming.py
```

### Manual Account ID Setup
```bash
# If you prefer to set account ID manually
# 1. Find your account ID in Schwab dashboard
# 2. Update .env file manually
# 3. Run streaming client
python schwab_streaming.py
```

## 📁 File Dependencies

The script uses these files:
- `.env` - Environment variables (API credentials)
- `schwab_token.json` - OAuth authentication token
- `schwab_streaming_env/` - Virtual environment with dependencies

## 🎯 Benefits

- **Automated**: No manual account ID lookup needed
- **Multiple Account Support**: Shows all available accounts
- **Smart Selection**: Automatically chooses appropriate account
- **Environment Integration**: Updates `.env` file automatically
- **Error Handling**: Clear guidance for issues
- **Integration**: Works seamlessly with streaming client

## 🔐 Security Notes

- **Token Security**: The script uses your existing OAuth token
- **Credential Safety**: Never hardcode credentials in the script
- **Environment Variables**: All sensitive data stored in `.env` file
- **Token File**: Keep `schwab_token.json` secure and don't share it

## 📚 Related Scripts

- `schwab_streaming.py` - Main streaming client
- `setup_schwab_streaming.py` - Initial setup and installation
- `simple_streaming_test.py` - Configuration testing
- `demo_streaming.py` - Demo with mock data

## 🚀 Next Steps

After successfully retrieving your account ID:

1. **Verify .env file** has the correct account ID
2. **Run streaming client**: `python schwab_streaming.py`
3. **Stream real-time data** for your selected symbols
4. **Enjoy live market data** from Schwab API!
