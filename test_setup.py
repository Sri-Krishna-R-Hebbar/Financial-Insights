"""
Test script to verify installation and API connectivity.
Run this before starting the main application.
"""

import os
import sys
from dotenv import load_dotenv

print("=" * 60)
print("Financial Insights - Setup Verification")
print("=" * 60)

# Load environment variables
load_dotenv()

# Track issues
issues = []
successes = []

# 1. Check Python version
print("\n1. Checking Python version...")
if sys.version_info >= (3, 8):
    successes.append(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    issues.append(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} (3.8+ required)")

# 2. Check required packages
print("\n2. Checking required packages...")
required_packages = [
    'streamlit',
    'langchain',
    'dotenv',
    'yfinance',
    'requests',
    'pandas'
]

for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        successes.append(f"✅ {package}")
    except ImportError:
        issues.append(f"❌ {package} not installed")

# 3. Check LLM API keys
print("\n3. Checking LLM API keys...")
google_key = os.getenv("GOOGLE_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if google_key:
    successes.append(f"✅ GOOGLE_API_KEY configured ({len(google_key)} chars)")
elif groq_key:
    successes.append(f"✅ GROQ_API_KEY configured ({len(groq_key)} chars)")
else:
    issues.append("❌ No LLM API key found (GOOGLE_API_KEY or GROQ_API_KEY required)")

# 4. Check ExchangeRate API
print("\n4. Checking ExchangeRate API key...")
exchange_key = os.getenv("EXCHANGERATE_API_KEY")
if exchange_key:
    successes.append(f"✅ EXCHANGERATE_API_KEY configured ({len(exchange_key)} chars)")
else:
    issues.append("⚠️  EXCHANGERATE_API_KEY not configured (currency data unavailable)")

# 5. Check Google Maps API
print("\n5. Checking Google Maps API key...")
maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
if maps_key:
    successes.append(f"✅ GOOGLE_MAPS_API_KEY configured ({len(maps_key)} chars)")
else:
    issues.append("⚠️  GOOGLE_MAPS_API_KEY not configured (maps unavailable)")

# 6. Test API connectivity
print("\n6. Testing API connectivity...")

# Test ExchangeRate API
if exchange_key:
    try:
        import requests
        response = requests.get(
            f"https://v6.exchangerate-api.com/v6/{exchange_key}/latest/USD",
            timeout=5
        )
        if response.status_code == 200:
            successes.append("✅ ExchangeRate-API connection successful")
        else:
            issues.append(f"❌ ExchangeRate-API returned status {response.status_code}")
    except Exception as e:
        issues.append(f"❌ ExchangeRate-API connection failed: {str(e)}")

# Test Yahoo Finance
try:
    import yfinance as yf
    ticker = yf.Ticker("^GSPC")
    hist = ticker.history(period="1d")
    if not hist.empty:
        successes.append("✅ Yahoo Finance connection successful")
    else:
        issues.append("⚠️  Yahoo Finance returned no data")
except Exception as e:
    issues.append(f"❌ Yahoo Finance connection failed: {str(e)}")

# 7. Test MCP tools
print("\n7. Testing MCP tools...")

try:
    from mcp.currency_tools import CurrencyMCPTool
    currency_tool = CurrencyMCPTool()
    result = currency_tool.get_country_currency("Japan")
    if "currency_code" in result:
        successes.append("✅ Currency MCP tool working")
    else:
        issues.append("❌ Currency MCP tool failed")
except Exception as e:
    issues.append(f"❌ Currency MCP tool error: {str(e)}")

try:
    from mcp.stock_tools import StockMCPTool
    stock_tool = StockMCPTool()
    result = stock_tool.get_exchange_info("Japan")
    if "exchanges" in result:
        successes.append("✅ Stock MCP tool working")
    else:
        issues.append("❌ Stock MCP tool failed")
except Exception as e:
    issues.append(f"❌ Stock MCP tool error: {str(e)}")

try:
    from mcp.maps_tools import GoogleMapsMCPTool
    maps_tool = GoogleMapsMCPTool()
    result = maps_tool.get_location_info("Tokyo Stock Exchange")
    if "exchange" in result:
        successes.append("✅ Maps MCP tool working")
    else:
        issues.append("❌ Maps MCP tool failed")
except Exception as e:
    issues.append(f"❌ Maps MCP tool error: {str(e)}")

# 8. Test LangChain agent initialization
print("\n8. Testing LangChain agent...")

if google_key or groq_key:
    try:
        from agent.agent import create_financial_agent
        provider = "google" if google_key else "groq"
        model = "gemini-pro" if google_key else "llama3-70b-8192"
        
        agent = create_financial_agent(model_name=model, provider=provider)
        successes.append(f"✅ LangChain agent initialized ({provider}/{model})")
    except Exception as e:
        issues.append(f"❌ LangChain agent initialization failed: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"\n✅ Successes: {len(successes)}")
for success in successes:
    print(f"  {success}")

if issues:
    print(f"\n⚠️  Issues: {len(issues)}")
    for issue in issues:
        print(f"  {issue}")
else:
    print("\n🎉 All checks passed! You're ready to run the application.")

print("\n" + "=" * 60)

if any("❌" in issue for issue in issues):
    print("\n⚠️  Critical issues found. Please fix them before running the app.")
    print("\nTo run the app:")
    print("  streamlit run app.py")
    sys.exit(1)
else:
    print("\n✅ Setup verification complete!")
    print("\nTo run the app:")
    print("  streamlit run app.py")
    sys.exit(0)
