"""
Stock Market Tools using Yahoo Finance.
Real-time stock market data via MCP protocol.
"""

import yfinance as yf
from typing import Dict, Any, List
import pandas as pd


class StockMCPTool:
    """MCP-compliant tool for stock market data."""
    
    def __init__(self):
        self.stock_exchanges = {
            "japan": {
                "exchanges": ["Tokyo Stock Exchange (TSE)", "Osaka Exchange (OSE)"],
                "indices": {
                    "Nikkei 225": "^N225",
                    "TOPIX": "^TOPX",
                    "JPX-Nikkei 400": "^JPN400"
                },
                "primary_exchange": "Tokyo Stock Exchange",
                "hq_location": "Tokyo, Japan"
            },
            "india": {
                "exchanges": ["National Stock Exchange (NSE)", "Bombay Stock Exchange (BSE)"],
                "indices": {
                    "NIFTY 50": "^NSEI",
                    "SENSEX": "^BSESN",
                    "NIFTY Bank": "^NSEBANK"
                },
                "primary_exchange": "National Stock Exchange of India",
                "hq_location": "Mumbai, Maharashtra, India"
            },
            "united states": {
                "exchanges": ["New York Stock Exchange (NYSE)", "NASDAQ", "CBOE"],
                "indices": {
                    "S&P 500": "^GSPC",
                    "Dow Jones": "^DJI",
                    "NASDAQ Composite": "^IXIC",
                    "Russell 2000": "^RUT"
                },
                "primary_exchange": "New York Stock Exchange",
                "hq_location": "New York, NY, USA"
            },
            "usa": {
                "exchanges": ["New York Stock Exchange (NYSE)", "NASDAQ", "CBOE"],
                "indices": {
                    "S&P 500": "^GSPC",
                    "Dow Jones": "^DJI",
                    "NASDAQ Composite": "^IXIC",
                    "Russell 2000": "^RUT"
                },
                "primary_exchange": "New York Stock Exchange",
                "hq_location": "New York, NY, USA"
            },
            "united kingdom": {
                "exchanges": ["London Stock Exchange (LSE)"],
                "indices": {
                    "FTSE 100": "^FTSE",
                    "FTSE 250": "^FTMC",
                    "FTSE All-Share": "^FTAS"
                },
                "primary_exchange": "London Stock Exchange",
                "hq_location": "London, United Kingdom"
            },
            "uk": {
                "exchanges": ["London Stock Exchange (LSE)"],
                "indices": {
                    "FTSE 100": "^FTSE",
                    "FTSE 250": "^FTMC"
                },
                "primary_exchange": "London Stock Exchange",
                "hq_location": "London, United Kingdom"
            },
            "south korea": {
                "exchanges": ["Korea Exchange (KRX)"],
                "indices": {
                    "KOSPI": "^KS11",
                    "KOSDAQ": "^KQ11"
                },
                "primary_exchange": "Korea Exchange",
                "hq_location": "Seoul, South Korea"
            },
            "korea": {
                "exchanges": ["Korea Exchange (KRX)"],
                "indices": {
                    "KOSPI": "^KS11",
                    "KOSDAQ": "^KQ11"
                },
                "primary_exchange": "Korea Exchange",
                "hq_location": "Seoul, South Korea"
            },
            "china": {
                "exchanges": ["Shanghai Stock Exchange (SSE)", "Shenzhen Stock Exchange (SZSE)", "Hong Kong Stock Exchange (HKEX)"],
                "indices": {
                    "SSE Composite": "000001.SS",
                    "Shenzhen Component": "399001.SZ",
                    "Hang Seng": "^HSI"
                },
                "primary_exchange": "Shanghai Stock Exchange",
                "hq_location": "Shanghai, China"
            },
            "germany": {
                "exchanges": ["Frankfurt Stock Exchange (FWB)"],
                "indices": {
                    "DAX": "^GDAXI",
                    "MDAX": "^MDAXI",
                    "TecDAX": "^TECDAX"
                },
                "primary_exchange": "Frankfurt Stock Exchange",
                "hq_location": "Frankfurt, Germany"
            },
            "france": {
                "exchanges": ["Euronext Paris"],
                "indices": {
                    "CAC 40": "^FCHI"
                },
                "primary_exchange": "Euronext Paris",
                "hq_location": "Paris, France"
            },
            "canada": {
                "exchanges": ["Toronto Stock Exchange (TSX)"],
                "indices": {
                    "S&P/TSX Composite": "^GSPTSE",
                    "S&P/TSX 60": "^TX60"
                },
                "primary_exchange": "Toronto Stock Exchange",
                "hq_location": "Toronto, Ontario, Canada"
            },
            "australia": {
                "exchanges": ["Australian Securities Exchange (ASX)"],
                "indices": {
                    "ASX 200": "^AXJO",
                    "All Ordinaries": "^AORD"
                },
                "primary_exchange": "Australian Securities Exchange",
                "hq_location": "Sydney, NSW, Australia"
            },
            "hong kong": {
                "exchanges": ["Hong Kong Stock Exchange (HKEX)"],
                "indices": {
                    "Hang Seng": "^HSI",
                    "Hang Seng Tech": "^HSTECH"
                },
                "primary_exchange": "Hong Kong Stock Exchange",
                "hq_location": "Hong Kong"
            },
            "singapore": {
                "exchanges": ["Singapore Exchange (SGX)"],
                "indices": {
                    "Straits Times Index": "^STI"
                },
                "primary_exchange": "Singapore Exchange",
                "hq_location": "Singapore"
            },
            "brazil": {
                "exchanges": ["B3 - Brasil Bolsa Balcão"],
                "indices": {
                    "Bovespa": "^BVSP"
                },
                "primary_exchange": "B3 - Brasil Bolsa Balcão",
                "hq_location": "São Paulo, Brazil"
            },
            "switzerland": {
                "exchanges": ["SIX Swiss Exchange"],
                "indices": {
                    "SMI": "^SSMI"
                },
                "primary_exchange": "SIX Swiss Exchange",
                "hq_location": "Zurich, Switzerland"
            },
            "spain": {
                "exchanges": ["Bolsa de Madrid"],
                "indices": {
                    "IBEX 35": "^IBEX"
                },
                "primary_exchange": "Bolsa de Madrid",
                "hq_location": "Madrid, Spain"
            },
            "italy": {
                "exchanges": ["Borsa Italiana"],
                "indices": {
                    "FTSE MIB": "FTSEMIB.MI"
                },
                "primary_exchange": "Borsa Italiana",
                "hq_location": "Milan, Italy"
            },
            "netherlands": {
                "exchanges": ["Euronext Amsterdam"],
                "indices": {
                    "AEX": "^AEX"
                },
                "primary_exchange": "Euronext Amsterdam",
                "hq_location": "Amsterdam, Netherlands"
            },
            "sweden": {
                "exchanges": ["Nasdaq Stockholm"],
                "indices": {
                    "OMX Stockholm 30": "^OMX"
                },
                "primary_exchange": "Nasdaq Stockholm",
                "hq_location": "Stockholm, Sweden"
            },
            "russia": {
                "exchanges": ["Moscow Exchange (MOEX)"],
                "indices": {
                    "MOEX Russia Index": "IMOEX.ME"
                },
                "primary_exchange": "Moscow Exchange",
                "hq_location": "Moscow, Russia"
            },
            "mexico": {
                "exchanges": ["Mexican Stock Exchange (BMV)"],
                "indices": {
                    "IPC": "^MXX"
                },
                "primary_exchange": "Mexican Stock Exchange",
                "hq_location": "Mexico City, Mexico"
            },
            "thailand": {
                "exchanges": ["Stock Exchange of Thailand (SET)"],
                "indices": {
                    "SET Index": "^SET.BK"
                },
                "primary_exchange": "Stock Exchange of Thailand",
                "hq_location": "Bangkok, Thailand"
            },
            "indonesia": {
                "exchanges": ["Indonesia Stock Exchange (IDX)"],
                "indices": {
                    "Jakarta Composite": "^JKSE"
                },
                "primary_exchange": "Indonesia Stock Exchange",
                "hq_location": "Jakarta, Indonesia"
            },
            "malaysia": {
                "exchanges": ["Bursa Malaysia"],
                "indices": {
                    "KLCI": "^KLSE"
                },
                "primary_exchange": "Bursa Malaysia",
                "hq_location": "Kuala Lumpur, Malaysia"
            },
        }
    
    def get_exchange_info(self, country_name: str) -> Dict[str, Any]:
        """
        Get stock exchange information for a country.
        
        Args:
            country_name: Name of the country
            
        Returns:
            Dict with exchange names, indices, and location
        """
        country_lower = country_name.lower().strip()
        
        if country_lower not in self.stock_exchanges:
            return {"error": f"Stock exchange information not found for country: {country_name}"}
        
        exchange_data = self.stock_exchanges[country_lower]
        
        return {
            "country": country_name.title(),
            "exchanges": exchange_data["exchanges"],
            "indices": list(exchange_data["indices"].keys()),
            "primary_exchange": exchange_data["primary_exchange"],
            "hq_location": exchange_data["hq_location"]
        }
    
    def get_index_values(self, country_name: str) -> Dict[str, Any]:
        """
        Get current/latest values for major stock indices of a country.
        
        Args:
            country_name: Name of the country
            
        Returns:
            Dict with index names and their current values
        """
        country_lower = country_name.lower().strip()
        
        if country_lower not in self.stock_exchanges:
            return {"error": f"Stock exchange information not found for country: {country_name}"}
        
        indices = self.stock_exchanges[country_lower]["indices"]
        index_data = {}
        
        for index_name, ticker_symbol in indices.items():
            try:
                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info
                hist = ticker.history(period="5d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    previous_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100 if previous_close else 0
                    
                    index_data[index_name] = {
                        "symbol": ticker_symbol,
                        "current_value": round(current_price, 2),
                        "previous_close": round(previous_close, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "last_updated": hist.index[-1].strftime("%Y-%m-%d %H:%M:%S")
                    }
                else:
                    index_data[index_name] = {
                        "symbol": ticker_symbol,
                        "error": "No data available"
                    }
                    
            except Exception as e:
                index_data[index_name] = {
                    "symbol": ticker_symbol,
                    "error": f"Failed to fetch data: {str(e)}"
                }
        
        return {
            "country": country_name.title(),
            "indices": index_data
        }
    
    def get_complete_stock_info(self, country_name: str) -> Dict[str, Any]:
        """
        Get complete stock market information for a country.
        
        Args:
            country_name: Name of the country
            
        Returns:
            Complete stock exchange and index information
        """
        exchange_info = self.get_exchange_info(country_name)
        
        if "error" in exchange_info:
            return exchange_info
        
        index_values = self.get_index_values(country_name)
        
        return {
            "country": exchange_info["country"],
            "exchanges": exchange_info["exchanges"],
            "primary_exchange": exchange_info["primary_exchange"],
            "hq_location": exchange_info["hq_location"],
            "indices": index_values.get("indices", {})
        }


# Standalone function for LangChain tool
def get_stock_market_info(country_name: str) -> str:
    """
    Get stock market information including exchanges and index values for a country.
    
    Args:
        country_name: Name of the country
        
    Returns:
        Formatted string with stock market information
    """
    tool = StockMCPTool()
    result = tool.get_complete_stock_info(country_name)
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    output = f"**Stock Market Information for {result['country']}**\n\n"
    
    output += "**Stock Exchanges:**\n"
    for exchange in result["exchanges"]:
        output += f"- {exchange}\n"
    
    output += f"\n**Primary Exchange:** {result['primary_exchange']}\n"
    output += f"**Headquarters Location:** {result['hq_location']}\n\n"
    
    output += "**Major Stock Indices:**\n\n"
    for index_name, index_info in result["indices"].items():
        if "error" in index_info:
            output += f"**{index_name}** ({index_info['symbol']}): {index_info['error']}\n\n"
        else:
            change_symbol = "▲" if index_info['change'] >= 0 else "▼"
            output += f"**{index_name}** ({index_info['symbol']})\n"
            output += f"- Current Value: {index_info['current_value']:,.2f}\n"
            output += f"- Change: {change_symbol} {abs(index_info['change']):,.2f} ({index_info['change_percent']:+.2f}%)\n"
            output += f"- Previous Close: {index_info['previous_close']:,.2f}\n"
            output += f"- Last Updated: {index_info['last_updated']}\n\n"
    
    return output
