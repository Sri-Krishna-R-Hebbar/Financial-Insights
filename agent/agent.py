"""
LangChain Agent with MCP Tools for Financial Information.
Simple implementation compatible with all LangChain versions.
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from agent.prompts import get_system_prompt
from mcp.server import get_currency_info, get_stock_market_info, get_exchange_location

load_dotenv()


class FinancialAgent:
    """
    Simple Financial Information Agent.
    Uses MCP tools for real-time data access without complex agent framework.
    """
    
    def __init__(self, model_name: Optional[str] = None, provider: Optional[str] = None):
        """
        Initialize the financial agent.
        
        Args:
            model_name: Name of the LLM model (e.g., 'gemini-pro', 'llama3-70b-8192')
            provider: LLM provider ('google', 'groq')
        """
        self.model_name = model_name or os.getenv("LLM_MODEL", "gemini-pro")
        self.provider = provider or os.getenv("LLM_PROVIDER", "google")
        
        # Initialize LLM
        self.llm = self._initialize_llm()
        
        # Track execution steps
        self.intermediate_steps = []
    
    def _initialize_llm(self):
        """Initialize the LLM based on provider."""
        
        if self.provider.lower() == "google":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            return ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=api_key,
                temperature=0.1,
                convert_system_message_to_human=True
            )
        
        elif self.provider.lower() == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            return ChatGroq(
                model=self.model_name,
                groq_api_key=api_key,
                temperature=0.1
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _extract_country_name(self, user_input: str) -> str:
        """Extract country name from user input."""
        # Simple extraction - look for common patterns
        user_input_lower = user_input.lower()
        
        # Remove common phrases
        for phrase in ["give me", "show me", "get", "details for", "information about", 
                       "currency and stock market details for", "financial information for"]:
            user_input_lower = user_input_lower.replace(phrase, "")
        
        # Clean up
        country = user_input_lower.strip()
        
        # Capitalize first letter of each word
        return country.title()
    
    def _call_tools(self, country: str) -> Dict[str, Any]:
        """Call all MCP tools for a country and collect results."""
        results = {}
        self.intermediate_steps = []
        
        # Step 1: Get currency info
        try:
            print(f"Calling get_currency_info for {country}...")
            currency_result = get_currency_info(country)
            results["currency_info"] = currency_result
            self.intermediate_steps.append({
                "tool": "get_currency_info",
                "input": country,
                "output": currency_result[:200] + "..." if len(currency_result) > 200 else currency_result
            })
        except Exception as e:
            results["currency_info"] = f"Error fetching currency info: {str(e)}"
            self.intermediate_steps.append({
                "tool": "get_currency_info",
                "input": country,
                "error": str(e)
            })
        
        # Step 2: Get stock market info
        try:
            print(f"Calling get_stock_market_info for {country}...")
            stock_result = get_stock_market_info(country)
            results["stock_info"] = stock_result
            self.intermediate_steps.append({
                "tool": "get_stock_market_info",
                "input": country,
                "output": stock_result[:200] + "..." if len(stock_result) > 200 else stock_result
            })
            
            # Extract primary exchange name for maps
            if "Primary Exchange:" in stock_result:
                lines = stock_result.split("\n")
                for line in lines:
                    if "Primary Exchange:" in line:
                        exchange_name = line.replace("**Primary Exchange:**", "").strip()
                        results["primary_exchange"] = exchange_name
                        break
        except Exception as e:
            results["stock_info"] = f"Error fetching stock info: {str(e)}"
            self.intermediate_steps.append({
                "tool": "get_stock_market_info",
                "input": country,
                "error": str(e)
            })
        
        # Step 3: Get exchange location if we have a primary exchange (OPTIONAL - only if Google Maps API key exists)
        if "primary_exchange" in results and os.getenv("GOOGLE_MAPS_API_KEY"):
            try:
                print(f"Calling get_exchange_location for {results['primary_exchange']}...")
                location_result = get_exchange_location(results['primary_exchange'])
                results["location_info"] = location_result
                self.intermediate_steps.append({
                    "tool": "get_exchange_location",
                    "input": results['primary_exchange'],
                    "output": str(location_result)
                })
            except Exception as e:
                results["location_info"] = {"error": str(e)}
                self.intermediate_steps.append({
                    "tool": "get_exchange_location",
                    "input": results.get('primary_exchange', ''),
                    "error": str(e)
                })
        
        return results
    
    def _format_output(self, country: str, results: Dict[str, Any]) -> str:
        """Format the tool results into a nice output."""
        output = f"# Financial Information for {country}\n\n"
        
        # Add currency information
        if "currency_info" in results:
            output += results["currency_info"] + "\n\n"
        
        # Add stock market information
        if "stock_info" in results:
            output += results["stock_info"] + "\n\n"
        
        # Add location information
        if "location_info" in results and "error" not in results["location_info"]:
            location = results["location_info"]
            output += "---\n\n"
            output += f"**Stock Exchange Location:**\n\n"
            if "exchange" in location:
                output += f"Exchange: {location['exchange']}\n\n"
            if "address" in location:
                output += f"Address: {location['address']}\n\n"
        
        return output
    
    def query(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user query and return financial information.
        
        Args:
            user_input: User's question/query
            
        Returns:
            Dict with output and intermediate steps
        """
        try:
            # Extract country name from query
            country = self._extract_country_name(user_input)
            
            if not country:
                return {
                    "success": False,
                    "error": "Could not identify country from query",
                    "output": "Please specify a country name in your query."
                }
            
            print(f"Processing query for country: {country}")
            
            # Call all tools
            results = self._call_tools(country)
            
            # Format output
            output = self._format_output(country, results)
            
            return {
                "success": True,
                "output": output,
                "intermediate_steps": self.intermediate_steps
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": f"Error processing query: {str(e)}"
            }
    
    def get_financial_info(self, country: str) -> Dict[str, Any]:
        """
        Get comprehensive financial information for a country.
        
        Args:
            country: Name of the country
            
        Returns:
            Dict with complete financial information
        """
        try:
            print(f"Getting financial info for: {country}")
            
            # Call all tools directly
            results = self._call_tools(country)
            
            # Format output
            output = self._format_output(country, results)
            
            return {
                "success": True,
                "output": output,
                "intermediate_steps": self.intermediate_steps
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": f"Error getting financial info: {str(e)}"
            }


def create_financial_agent(model_name: Optional[str] = None, provider: Optional[str] = None) -> FinancialAgent:
    """
    Create a financial agent instance.
    
    Args:
        model_name: Name of the LLM model
        provider: LLM provider ('google', 'groq')
        
    Returns:
        FinancialAgent instance
    """
    return FinancialAgent(model_name=model_name, provider=provider)
