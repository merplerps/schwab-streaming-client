# How to Find Your Schwab Account ID

## 🔍 Finding Your Schwab Account ID

The Schwab Streaming Client requires your account ID to stream real-time market data. Here's how to find it:

### Method 1: Schwab Website (Easiest)

1. **Log in to Schwab.com**
2. **Go to your account dashboard**
3. **Look for your account number** - it's usually displayed prominently
4. **Copy the account number** (it's typically 8-10 digits)

### Method 2: Schwab Mobile App

1. **Open the Schwab mobile app**
2. **Go to your account summary**
3. **Your account number should be visible** at the top of the screen

### Method 3: Account Statements

1. **Check your monthly account statements**
2. **Look for "Account Number"** at the top of the statement
3. **Copy the account number**

### Method 4: Schwab API (Advanced)

If you have API access working, you can retrieve it programmatically:

```python
# This would be in a separate script once you have API access
from schwab.auth import easy_client

client = easy_client(
    api_key='your_api_key',
    app_secret='your_app_secret',
    callback_url='https://127.0.0.1:8182',
    token_path='schwab_token.json'
)

# Get user principals to find account info
principals = client.get_user_principals()
accounts = principals.json().get('accounts', [])
for account in accounts:
    print(f"Account ID: {account.get('accountId')}")
```

## 📝 Setting Your Account ID

Once you have your account ID, update your `.env` file:

```env
SCHWAB_API_KEY=your_actual_api_key
SCHWAB_APP_SECRET=your_actual_app_secret
SCHWAB_ACCOUNT_ID=123456789  # Replace with your actual account ID
SCHWAB_REDIRECT_URI=https://127.0.0.1:8182
```

## 🎯 Account ID Format

- **Length**: Usually 8-10 digits
- **Format**: Numbers only (no dashes or spaces)
- **Example**: `123456789` or `9876543210`

## ⚠️ Important Notes

- **Don't confuse with routing number**: Your account ID is different from your bank routing number
- **Multiple accounts**: If you have multiple Schwab accounts, use the one you want to stream data for
- **Keep it secure**: Don't share your account ID publicly

## 🚀 After Setting Account ID

Once you've set your account ID in the `.env` file:

```bash
# Activate the virtual environment
source schwab_streaming_env/bin/activate

# Run the streaming client
python schwab_streaming.py
```

The client will now be able to authenticate and stream real-time market data!
