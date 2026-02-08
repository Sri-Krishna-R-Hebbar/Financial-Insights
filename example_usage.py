"""
Example Usage - Financial Insights Agent
Demonstrates how to use the MCP tools and agent programmatically.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("Financial Insights Agent - Example Usage")
print("=" * 70)


# Example 1: Using MCP Tools Directly
print("\n" + "=" * 70)
print("EXAMPLE 1: Using MCP Tools Directly")
print("=" * 70)

print("\n--- Currency Tool ---")
from mcp.currency_tools import get_currency_info

result = get_currency_info("Japan")
print(result)

print("\n--- Stock Market Tool ---")
from mcp.stock_tools import get_stock_market_info

result = get_stock_market_info("India")
print(result)

print("\n--- Google Maps Tool ---")
from mcp.maps_tools import get_exchange_location

result = get_exchange_location("New York Stock Exchange")
print(f"\nExchange: {result.get('exchange')}")
print(f"Address: {result.get('address')}")
print(f"Map URL: {result.get('map_url')}")


# Example 2: Using the LangChain Agent
print("\n\n" + "=" * 70)
print("EXAMPLE 2: Using the LangChain Agent")
print("=" * 70)

from agent.agent import create_financial_agent

# Initialize agent
print("\nInitializing agent...")
agent = create_financial_agent()
print("Agent initialized!")

# Query for a country
countries = ["Japan", "United Kingdom", "South Korea"]

for country in countries:
    print(f"\n--- Financial Information for {country} ---\n")
    
    result = agent.get_financial_info(country)
    
    if result["success"]:
        print(result["output"])
        
        # Show tool calls made
        print("\n--- Tool Calls ---")
        for idx, step in enumerate(result.get("intermediate_steps", []), 1):
            action = step[0]
            print(f"\nStep {idx}: {action.tool}")
            print(f"Input: {action.tool_input}")
    else:
        print(f"Error: {result.get('error')}")
    
    print("\n" + "-" * 70)


# Example 3: Custom Queries
print("\n\n" + "=" * 70)
print("EXAMPLE 3: Custom Queries")
print("=" * 70)

custom_queries = [
    "What is the currency of Germany and its exchange rate to USD?",
    "Show me the major stock indices for Canada",
    "Where is the London Stock Exchange located?"
]

for query in custom_queries:
    print(f"\nQuery: {query}")
    print("-" * 70)
    
    result = agent.query(query)
    
    if result["success"]:
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")
    
    print()


# Example 4: Using MCP Server Class
print("\n\n" + "=" * 70)
print("EXAMPLE 4: Using MCP Server Class")
print("=" * 70)

from mcp.server import MCPFinancialServer

server = MCPFinancialServer()

# List available tools
print("\n--- Available Tools ---")
tools = server.list_tools()
for tool in tools:
    print(f"\n{tool['name']}")
    print(f"Description: {tool['description']}")

# Execute a tool
print("\n\n--- Executing Tool: get_currency_info ---")
result = server.execute_tool("get_currency_info", {"country_name": "France"})
print(result)

print("\n\n--- Executing Tool: get_stock_market_info ---")
result = server.execute_tool("get_stock_market_info", {"country_name": "Singapore"})
print(result)


# Example 5: Batch Processing Multiple Countries
print("\n\n" + "=" * 70)
print("EXAMPLE 5: Batch Processing Multiple Countries")
print("=" * 70)

countries_batch = ["Japan", "India", "United States", "United Kingdom", "Germany"]

print("\nProcessing multiple countries...")
print("-" * 70)

results_summary = []

for country in countries_batch:
    print(f"\nProcessing {country}...")
    result = agent.get_financial_info(country)
    
    if result["success"]:
        results_summary.append({
            "country": country,
            "status": "✅ Success"
        })
    else:
        results_summary.append({
            "country": country,
            "status": f"❌ Failed: {result.get('error')}"
        })

print("\n\n--- Summary ---")
for item in results_summary:
    print(f"{item['country']}: {item['status']}")


print("\n\n" + "=" * 70)
print("Examples Complete!")
print("=" * 70)
print("\nTo run the interactive UI:")
print("  streamlit run app.py")
print()
