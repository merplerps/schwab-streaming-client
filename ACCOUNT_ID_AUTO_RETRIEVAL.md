# Automatic Account ID Retrieval

## 🎉 New Feature: Automatic Account ID Detection

The Schwab Streaming Client now automatically retrieves your account ID from the Schwab API, eliminating the need to manually find and enter your account ID.

## ✅ What's Changed

### Before (Manual Setup)
```env
# Required all three credentials
SCHWAB_API_KEY=your_api_key
SCHWAB_APP_SECRET=your_app_secret
SCHWAB_ACCOUNT_ID=your_account_id  # Had to find this manually
```

### After (Automatic Detection)
```env
# Only need API credentials - account ID is auto-retrieved
SCHWAB_API_KEY=your_api_key
SCHWAB_APP_SECRET=your_app_secret
# SCHWAB_ACCOUNT_ID=optional  # Will be retrieved automatically
```

## 🔧 How It Works

1. **Authentication**: Complete OAuth authentication with Schwab
2. **Account Discovery**: Client calls `get_user_principals()` API endpoint
3. **Account Selection**: 
   - If you have 1 account: Uses it automatically
   - If you have multiple accounts: Uses the first one
   - Shows all available accounts for reference
4. **Streaming**: Proceeds with the detected account ID

## 📋 Account Information Display

When the client retrieves account information, you'll see:

```
🔍 Retrieving account information from Schwab API...
📋 Found 2 account(s):
   1. Account ID: 123456789 (Type: CASH)
   2. Account ID: 987654321 (Type: MARGIN)
✅ Using first account: 123456789
💡 To use a different account, set SCHWAB_ACCOUNT_ID in your .env file
```

## 🎯 Benefits

- **Simplified Setup**: No need to find your account ID manually
- **Multiple Account Support**: Automatically handles multiple accounts
- **Error Prevention**: Eliminates account ID typos
- **Flexibility**: Still allows manual account ID specification if needed

## 🔧 Manual Override

If you want to use a specific account instead of the auto-detected one:

1. **Set in .env file**:
   ```env
   SCHWAB_ACCOUNT_ID=your_preferred_account_id
   ```

2. **The client will use your specified account ID instead of auto-detecting**

## 🧪 Testing

Test the account ID retrieval:

```bash
# Test account ID retrieval (requires valid credentials and OAuth)
python test_account_retrieval.py

# Test overall configuration
python simple_streaming_test.py
```

## 🚀 Usage

The streaming client works exactly the same way:

```bash
# Activate environment
source schwab_streaming_env/bin/activate

# Run streaming client (will auto-detect account ID)
python schwab_streaming.py

# Or with custom symbols
python schwab_streaming.py AAPL,GOOGL,MSFT
```

## 🔍 Troubleshooting

### No Accounts Found
```
❌ No accounts found in user principals
```
**Solution**: Ensure your Schwab account has API access enabled

### Multiple Accounts
```
📋 Found 3 account(s):
   1. Account ID: 111111111 (Type: CASH)
   2. Account ID: 222222222 (Type: MARGIN) 
   3. Account ID: 333333333 (Type: IRA)
```
**Solution**: The client uses the first account. To use a different one, set `SCHWAB_ACCOUNT_ID` in your `.env` file.

### API Errors
```
❌ Failed to get user principals: 401
```
**Solution**: Check your API credentials and ensure OAuth authentication is complete.

## 📚 Related Files

- `schwab_streaming.py` - Main streaming client with auto-detection
- `test_account_retrieval.py` - Test account ID retrieval
- `simple_streaming_test.py` - Test overall configuration
- `.env` - Environment configuration (account ID now optional)
