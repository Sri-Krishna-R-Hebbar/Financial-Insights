"""
MCP Server Entry Point
Provides Model Context Protocol compliant tools for financial data access.
"""

from mcp.currency_tools import CurrencyMCPTool, get_currency_info
from mcp.stock_tools import StockMCPTool, get_stock_market_info
from mcp.maps_tools import GoogleMapsMCPTool, get_exchange_location


class MCPFinancialServer:
    """
    MCP Server for financial information tools.
    Provides currency, stock market, and location data.
    """
    
    def __init__(self):
        self.currency_tool = CurrencyMCPTool()
        self.stock_tool = StockMCPTool()
        self.maps_tool = GoogleMapsMCPTool()
    
    def list_tools(self):
        """List all available MCP tools."""
        return [
            {
                "name": "get_currency_info",
                "description": "Get currency and exchange rate information for a country. Returns currency name, code, and real-time exchange rates to USD, EUR, GBP, and INR.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country_name": {
                            "type": "string",
                            "description": "Name of the country (e.g., 'Japan', 'India', 'United States')"
                        }
                    },
                    "required": ["country_name"]
                }
            },
            {
                "name": "get_stock_market_info",
                "description": "Get stock market information for a country including exchanges, major indices, and current index values from Yahoo Finance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country_name": {
                            "type": "string",
                            "description": "Name of the country (e.g., 'Japan', 'India', 'United States')"
                        }
                    },
                    "required": ["country_name"]
                }
            },
            {
                "name": "get_exchange_location",
                "description": "Get Google Maps location and embed URL for a stock exchange headquarters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "exchange_name": {
                            "type": "string",
                            "description": "Name of the stock exchange (e.g., 'Tokyo Stock Exchange', 'New York Stock Exchange')"
                        }
                    },
                    "required": ["exchange_name"]
                }
            }
        ]
    
    def execute_tool(self, tool_name: str, parameters: dict):
        """Execute an MCP tool with given parameters."""
        
        if tool_name == "get_currency_info":
            return get_currency_info(parameters.get("country_name", ""))
        
        elif tool_name == "get_stock_market_info":
            return get_stock_market_info(parameters.get("country_name", ""))
        
        elif tool_name == "get_exchange_location":
            return get_exchange_location(parameters.get("exchange_name", ""))
        
        else:
            return {"error": f"Unknown tool: {tool_name}"}


# Export tools for LangChain integration
__all__ = [
    'MCPFinancialServer',
    'get_currency_info',
    'get_stock_market_info',
    'get_exchange_location',
    'CurrencyMCPTool',
    'StockMCPTool',
    'GoogleMapsMCPTool'
]
