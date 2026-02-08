"""
Currency and Exchange Rate Tools using ExchangeRate-API.
Real-time currency data via MCP protocol.
"""

import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class CurrencyMCPTool:
    """MCP-compliant tool for currency exchange rates."""
    
    def __init__(self):
        self.api_key = os.getenv("EXCHANGERATE_API_KEY")
        self.base_url = "https://v6.exchangerate-api.com/v6"
        
    def get_country_currency(self, country_name: str) -> Dict[str, str]:
        """
        Get the official currency for a given country.
        
        Args:
            country_name: Name of the country
            
        Returns:
            Dict with currency_code and currency_name
        """
        # Country to currency code mapping (ISO 4217)
        country_currency_map = {
            "japan": {"code": "JPY", "name": "Japanese Yen"},
            "india": {"code": "INR", "name": "Indian Rupee"},
            "united states": {"code": "USD", "name": "US Dollar"},
            "usa": {"code": "USD", "name": "US Dollar"},
            "united kingdom": {"code": "GBP", "name": "British Pound Sterling"},
            "uk": {"code": "GBP", "name": "British Pound Sterling"},
            "south korea": {"code": "KRW", "name": "South Korean Won"},
            "korea": {"code": "KRW", "name": "South Korean Won"},
            "china": {"code": "CNY", "name": "Chinese Yuan"},
            "germany": {"code": "EUR", "name": "Euro"},
            "france": {"code": "EUR", "name": "Euro"},
            "italy": {"code": "EUR", "name": "Euro"},
            "spain": {"code": "EUR", "name": "Euro"},
            "canada": {"code": "CAD", "name": "Canadian Dollar"},
            "australia": {"code": "AUD", "name": "Australian Dollar"},
            "brazil": {"code": "BRL", "name": "Brazilian Real"},
            "mexico": {"code": "MXN", "name": "Mexican Peso"},
            "switzerland": {"code": "CHF", "name": "Swiss Franc"},
            "singapore": {"code": "SGD", "name": "Singapore Dollar"},
            "hong kong": {"code": "HKD", "name": "Hong Kong Dollar"},
            "russia": {"code": "RUB", "name": "Russian Ruble"},
            "south africa": {"code": "ZAR", "name": "South African Rand"},
            "turkey": {"code": "TRY", "name": "Turkish Lira"},
            "saudi arabia": {"code": "SAR", "name": "Saudi Riyal"},
            "uae": {"code": "AED", "name": "UAE Dirham"},
            "thailand": {"code": "THB", "name": "Thai Baht"},
            "malaysia": {"code": "MYR", "name": "Malaysian Ringgit"},
            "indonesia": {"code": "IDR", "name": "Indonesian Rupiah"},
            "philippines": {"code": "PHP", "name": "Philippine Peso"},
            "vietnam": {"code": "VND", "name": "Vietnamese Dong"},
            "poland": {"code": "PLN", "name": "Polish Zloty"},
            "sweden": {"code": "SEK", "name": "Swedish Krona"},
            "norway": {"code": "NOK", "name": "Norwegian Krone"},
            "denmark": {"code": "DKK", "name": "Danish Krone"},
            "new zealand": {"code": "NZD", "name": "New Zealand Dollar"},
            "argentina": {"code": "ARS", "name": "Argentine Peso"},
            "chile": {"code": "CLP", "name": "Chilean Peso"},
            "colombia": {"code": "COP", "name": "Colombian Peso"},
            "egypt": {"code": "EGP", "name": "Egyptian Pound"},
            "israel": {"code": "ILS", "name": "Israeli Shekel"},
            "pakistan": {"code": "PKR", "name": "Pakistani Rupee"},
            "bangladesh": {"code": "BDT", "name": "Bangladeshi Taka"},
            "nigeria": {"code": "NGN", "name": "Nigerian Naira"},
            "kenya": {"code": "KES", "name": "Kenyan Shilling"},
        }
        
        country_lower = country_name.lower().strip()
        currency_info = country_currency_map.get(country_lower)
        
        if not currency_info:
            return {"error": f"Currency information not found for country: {country_name}"}
        
        return {
            "country": country_name.title(),
            "currency_code": currency_info["code"],
            "currency_name": currency_info["name"]
        }
    
    def get_exchange_rates(self, base_currency: str, target_currencies: list) -> Dict[str, Any]:
        """
        Get real-time exchange rates from base currency to target currencies.
        
        Args:
            base_currency: Base currency code (e.g., 'JPY')
            target_currencies: List of target currency codes (e.g., ['USD', 'EUR', 'GBP', 'INR'])
            
        Returns:
            Dict with exchange rates and metadata
        """
        if not self.api_key:
            return {"error": "EXCHANGERATE_API_KEY not configured"}
        
        try:
            url = f"{self.base_url}/{self.api_key}/latest/{base_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("result") != "success":
                return {"error": f"API error: {data.get('error-type', 'Unknown error')}"}
            
            rates = {}
            conversion_rates = data.get("conversion_rates", {})
            
            for target in target_currencies:
                if target in conversion_rates:
                    rates[target] = conversion_rates[target]
                else:
                    rates[target] = "Not available"
            
            return {
                "base_currency": base_currency,
                "rates": rates,
                "last_updated": data.get("time_last_update_utc"),
                "next_update": data.get("time_next_update_utc")
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch exchange rates: {str(e)}"}
    
    def get_all_rates_for_country(self, country_name: str) -> Dict[str, Any]:
        """
        Get currency info and exchange rates for a country to USD, EUR, GBP, INR.
        
        Args:
            country_name: Name of the country
            
        Returns:
            Complete currency and exchange rate information
        """
        # Get country currency
        currency_info = self.get_country_currency(country_name)
        
        if "error" in currency_info:
            return currency_info
        
        # Get exchange rates
        base_currency = currency_info["currency_code"]
        target_currencies = ["USD", "EUR", "GBP", "INR"]
        
        # Remove base currency from targets if present
        if base_currency in target_currencies:
            target_currencies.remove(base_currency)
        
        exchange_data = self.get_exchange_rates(base_currency, target_currencies)
        
        return {
            "country": currency_info["country"],
            "currency_code": currency_info["currency_code"],
            "currency_name": currency_info["currency_name"],
            "exchange_rates": exchange_data
        }


# Standalone function for LangChain tool
def get_currency_info(country_name: str) -> str:
    """
    Get currency and exchange rate information for a country.
    
    Args:
        country_name: Name of the country
        
    Returns:
        Formatted string with currency information
    """
    tool = CurrencyMCPTool()
    result = tool.get_all_rates_for_country(country_name)
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    output = f"**Currency Information for {result['country']}**\n\n"
    output += f"Currency: {result['currency_name']} ({result['currency_code']})\n\n"
    
    if "exchange_rates" in result and "rates" in result["exchange_rates"]:
        output += "**Exchange Rates (1 {} = ):**\n".format(result['currency_code'])
        for currency, rate in result["exchange_rates"]["rates"].items():
            if isinstance(rate, (int, float)):
                output += f"- {currency}: {rate:.4f}\n"
            else:
                output += f"- {currency}: {rate}\n"
        
        if "last_updated" in result["exchange_rates"]:
            output += f"\nLast Updated: {result['exchange_rates']['last_updated']}\n"
    
    return output
