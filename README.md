# 💹 Financial Insights Agent

A complete end-to-end LLM-powered financial information agent that provides real-time currency exchange rates, stock market data, and stock exchange locations using the Model Context Protocol (MCP).

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1.9-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

- **Real-time Currency Information**: Fetch official currency names and live exchange rates
- **Stock Market Data**: Get information on major stock exchanges and indices with current values
- **Location Mapping**: View stock exchange headquarters on Google Maps
- **Multiple LLM Support**: Works with Gemini, LLaMA-3, Mistral, and other models
- **MCP Protocol**: All external data accessed via Model Context Protocol
- **Interactive UI**: Beautiful Streamlit interface with sample queries
- **No Mock Data**: All data fetched from real public APIs

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
┌────────▼────────┐
│ LangChain Agent │
└────────┬────────┘
         │
┌────────▼────────────────────────┐
│  MCP Tools (Protocol Layer)     │
├─────────────────────────────────┤
│ - Currency Tools                │
│ - Stock Market Tools            │
│ - Google Maps Tools             │
└────────┬────────────────────────┘
         │
┌────────▼────────────────────────┐
│  External APIs                  │
├─────────────────────────────────┤
│ - ExchangeRate-API              │
│ - Yahoo Finance (yfinance)      │
│ - Google Maps Embed API         │
└─────────────────────────────────┘
```

## 📁 Project Structure

```
Financial-Insights/
├── app.py                      # Streamlit UI application
├── agent/
│   ├── __init__.py
│   ├── agent.py               # LangChain agent logic
│   └── prompts.py             # System and user prompts
├── mcp/
│   ├── __init__.py
│   ├── server.py              # MCP server entry point
│   ├── currency_tools.py      # Currency & exchange rate tools
│   ├── stock_tools.py         # Yahoo Finance stock tools
│   └── maps_tools.py          # Google Maps location tools
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- API Keys (see Configuration section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Financial-Insights.git
   cd Financial-Insights
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit .env and add your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 🔑 Configuration

### Required API Keys

1. **LLM API Key** (choose one):
   - **Google Gemini**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **Groq**: Get from [Groq Console](https://console.groq.com/keys)

2. **ExchangeRate-API**: Get free key from [ExchangeRate-API](https://www.exchangerate-api.com/)
   - Free tier: 1,500 requests/month
   - No credit card required

3. **Google Maps API**: Get from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Enable "Maps Embed API"
   - Free tier: $200 credit/month

### Environment Variables (.env)

```bash
# LLM Configuration (choose one or more)
GOOGLE_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Currency Exchange API
EXCHANGERATE_API_KEY=your_exchangerate_api_key_here

# Google Maps API
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# LLM Model Selection
LLM_MODEL=gemini-pro
LLM_PROVIDER=google
```

### Supported LLM Models

**Google (Gemini)**:
- `gemini-pro` (recommended)
- `gemini-1.5-pro`
- `gemini-1.5-flash`

**Groq**:
- `llama3-70b-8192` (recommended)
- `llama3-8b-8192`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

## 📖 Usage

### Basic Usage

1. Launch the application:
   ```bash
   streamlit run app.py
   ```

2. Enter a country name in the input field

3. Click "Get Financial Details"

4. View the results including:
   - Currency information
   - Exchange rates
   - Stock exchanges and indices
   - Current index values
   - Stock exchange location map

### Sample Queries

Try these countries:

- **Japan** 🇯🇵
  - Currency: Japanese Yen (JPY)
  - Indices: Nikkei 225, TOPIX
  - Exchange: Tokyo Stock Exchange

- **India** 🇮🇳
  - Currency: Indian Rupee (INR)
  - Indices: NIFTY 50, SENSEX
  - Exchange: National Stock Exchange of India

- **United States** 🇺🇸
  - Currency: US Dollar (USD)
  - Indices: S&P 500, Dow Jones, NASDAQ
  - Exchange: New York Stock Exchange

- **United Kingdom** 🇬🇧
  - Currency: British Pound Sterling (GBP)
  - Indices: FTSE 100, FTSE 250
  - Exchange: London Stock Exchange

- **South Korea** 🇰🇷
  - Currency: South Korean Won (KRW)
  - Indices: KOSPI, KOSDAQ
  - Exchange: Korea Exchange

- **China** 🇨🇳
  - Currency: Chinese Yuan (CNY)
  - Indices: SSE Composite, Hang Seng
  - Exchange: Shanghai Stock Exchange

### Advanced Usage

**Custom Queries**: You can ask natural language questions like:
- "Give me currency and stock market details for Japan"
- "What are the exchange rates for India?"
- "Show me stock indices for Germany"

**Model Selection**: Use the sidebar to:
- Switch between Google Gemini and Groq
- Select different model sizes
- View API key status

## 🔧 MCP Tools

### 1. Currency Tool (`currency_tools.py`)

**Data Source**: ExchangeRate-API

**Features**:
- Get official currency name and code for any country
- Real-time exchange rates to USD, EUR, GBP, INR
- Last update timestamp
- Support for 50+ countries

**Example**:
```python
from mcp.currency_tools import get_currency_info

result = get_currency_info("Japan")
# Returns currency name, code, and exchange rates
```

### 2. Stock Market Tool (`stock_tools.py`)

**Data Source**: Yahoo Finance (yfinance)

**Features**:
- List of major stock exchanges
- Major stock indices with symbols
- Current index values
- Price changes and percentages
- Primary exchange location

**Example**:
```python
from mcp.stock_tools import get_stock_market_info

result = get_stock_market_info("India")
# Returns exchange info, indices, and current values
```

### 3. Google Maps Tool (`maps_tools.py`)

**Data Source**: Google Maps Embed API

**Features**:
- Stock exchange headquarters location
- Address and coordinates
- Embedded map iframe
- Support for 20+ major exchanges

**Example**:
```python
from mcp.maps_tools import get_exchange_location

result = get_exchange_location("Tokyo Stock Exchange")
# Returns address, coordinates, and map embed URL
```

## 🎯 Agent Behavior

The LangChain agent follows this workflow:

1. **Parse Query**: Extract country name from user input
2. **Identify Currency**: Determine official currency code
3. **Fetch Currency Data**: Call `get_currency_info` tool
4. **Fetch Stock Data**: Call `get_stock_market_info` tool
5. **Fetch Location Data**: Call `get_exchange_location` tool
6. **Synthesize Response**: Combine all data into structured output

The agent uses the system prompt in `agent/prompts.py` to guide its behavior and ensure consistent, high-quality responses.

## 📊 Supported Countries

The application currently supports 50+ countries including:

**Asia-Pacific**: Japan, India, China, South Korea, Hong Kong, Singapore, Australia, Thailand, Indonesia, Malaysia, Philippines, Vietnam, New Zealand

**Americas**: United States, Canada, Brazil, Mexico, Argentina, Chile, Colombia

**Europe**: United Kingdom, Germany, France, Italy, Spain, Netherlands, Switzerland, Sweden, Norway, Denmark, Poland, Russia, Turkey

**Middle East & Africa**: UAE, Saudi Arabia, Israel, Egypt, South Africa, Nigeria, Kenya

## 🛠️ Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

### Code Style

```bash
# Install development dependencies
pip install black flake8 isort

# Format code
black .

# Check style
flake8 .

# Sort imports
isort .
```

### Adding New Countries

Edit `mcp/currency_tools.py` and `mcp/stock_tools.py`:

```python
# In currency_tools.py
country_currency_map = {
    "new_country": {
        "code": "XXX",
        "name": "Currency Name"
    }
}

# In stock_tools.py
stock_exchanges = {
    "new_country": {
        "exchanges": ["Exchange Name"],
        "indices": {"Index Name": "^SYMBOL"},
        "primary_exchange": "Primary Exchange",
        "hq_location": "City, Country"
    }
}
```

## 🔒 Security & Privacy

- **API Keys**: Never commit `.env` file to version control
- **Rate Limits**: Respect API rate limits (configured in tools)
- **Data Privacy**: No user data is stored or logged
- **HTTPS**: All API calls use secure HTTPS connections

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**2. API Key Not Found**
```bash
# Check .env file exists
ls -la .env

# Verify API keys are set
cat .env
```

**3. Yahoo Finance Data Unavailable**
- Some indices may have delayed data
- Check internet connection
- Verify ticker symbols are correct

**4. Google Maps Not Loading**
- Verify GOOGLE_MAPS_API_KEY is configured
- Check Maps Embed API is enabled in Google Cloud Console
- Verify billing is enabled (free tier available)

**5. LLM Rate Limits**
- Switch to a different model
- Wait a few minutes and retry
- Check API quota in provider console

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the agent framework
- [Streamlit](https://streamlit.io/) for the UI framework
- [ExchangeRate-API](https://www.exchangerate-api.com/) for currency data
- [Yahoo Finance](https://finance.yahoo.com/) for stock market data
- [Google Maps](https://developers.google.com/maps) for location services

## 📚 References

- [Model Context Protocol Specification](https://github.com/anthropics/mcp)
- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)

---

**Built with ❤️ using Python, Streamlit, LangChain, and MCP**
