"""
Financial Insights - Streamlit Application
LLM-powered financial information agent using MCP protocol.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from agent.agent import create_financial_agent
from mcp.maps_tools import GoogleMapsMCPTool

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Financial Insights Agent",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff4444;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #44ff44;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'map_location' not in st.session_state:
        st.session_state.map_location = None


def check_api_keys():
    """Check if required API keys are configured."""
    issues = []
    
    # Check LLM API keys
    google_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not google_key and not groq_key:
        issues.append("❌ No LLM API key found. Please configure GOOGLE_API_KEY or GROQ_API_KEY")
    
    # Check Exchange Rate API
    if not os.getenv("EXCHANGERATE_API_KEY"):
        issues.append("⚠️ EXCHANGERATE_API_KEY not configured. Currency data may not be available.")
    
    # Check Google Maps API (OPTIONAL)
    if not os.getenv("GOOGLE_MAPS_API_KEY"):
        issues.append("ℹ️ GOOGLE_MAPS_API_KEY not configured (optional). Maps will not be displayed.")
    
    return issues


def display_header():
    """Display the application header."""
    st.markdown('<div class="main-header">💹 Financial Insights Agent</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Real-time Currency & Stock Market Information via Model Context Protocol</div>',
        unsafe_allow_html=True
    )


def display_sidebar():
    """Display sidebar configuration."""
    st.sidebar.title("⚙️ Configuration")
    
    # API Key Status
    st.sidebar.subheader("🔑 API Key Status")
    issues = check_api_keys()
    
    if not issues:
        st.sidebar.markdown('<div class="success-box">✅ All API keys configured</div>', unsafe_allow_html=True)
    else:
        for issue in issues:
            st.sidebar.warning(issue)
    
    st.sidebar.markdown("---")
    
    # Model Selection
    st.sidebar.subheader("🤖 LLM Configuration")
    
    provider = st.sidebar.selectbox(
        "Provider",
        options=["google", "groq"],
        index=0,
        help="Select the LLM provider"
    )
    
    if provider == "google":
        model_options = ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
        default_model = "gemini-pro"
    else:  # groq
        model_options = [
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]
        default_model = "llama3-70b-8192"
    
    model = st.sidebar.selectbox(
        "Model",
        options=model_options,
        index=0,
        help="Select the LLM model"
    )
    
    st.sidebar.markdown("---")
    
    # About Section
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.info(
        """
        This agent uses:
        - **LangChain** for agent orchestration
        - **MCP Protocol** for data access
        - **ExchangeRate-API** for currency data
        - **Yahoo Finance** for stock data
        - **Google Maps** for locations
        
        All data is fetched in real-time from public APIs.
        """
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Built with ❤️ using Streamlit")
    
    return provider, model


def display_sample_queries():
    """Display sample query buttons."""
    st.markdown('<div class="section-header">📝 Sample Queries</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    sample_countries = [
        ("🇯🇵 Japan", "Japan"),
        ("🇮🇳 India", "India"),
        ("🇺🇸 United States", "United States"),
        ("🇬🇧 United Kingdom", "United Kingdom"),
        ("🇰🇷 South Korea", "South Korea"),
        ("🇨🇳 China", "China"),
        ("🇩🇪 Germany", "Germany"),
        ("🇫🇷 France", "France"),
        ("🇨🇦 Canada", "Canada")
    ]
    
    cols = [col1, col2, col3]
    for idx, (display_name, country) in enumerate(sample_countries):
        with cols[idx % 3]:
            if st.button(display_name, key=f"sample_{country}", use_container_width=True):
                st.session_state.selected_country = country
                st.rerun()


def parse_and_display_results(output: str, country: str):
    """Parse and display agent results in a structured format."""
    
    st.markdown('<div class="section-header">📊 Results</div>', unsafe_allow_html=True)
    
    # Display raw output in markdown
    st.markdown(output)
    
    # Try to extract and display map if available (OPTIONAL - only if Google Maps API key is configured)
    if os.getenv("GOOGLE_MAPS_API_KEY"):
        try:
            from mcp.stock_tools import StockMCPTool
            stock_tool = StockMCPTool()
            exchange_info = stock_tool.get_exchange_info(country)
            
            if "primary_exchange" in exchange_info:
                primary_exchange = exchange_info["primary_exchange"]
                
                st.markdown('<div class="section-header">🗺️ Stock Exchange Location</div>', unsafe_allow_html=True)
                
                maps_tool = GoogleMapsMCPTool()
                location_info = maps_tool.get_location_info(primary_exchange)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("**Exchange:**")
                    st.write(primary_exchange)
                    
                    if "address" in location_info:
                        st.markdown("**Address:**")
                        st.write(location_info["address"])
                    
                    if "coordinates" in location_info:
                        coords = location_info["coordinates"]
                        st.markdown("**Coordinates:**")
                        st.write(f"Lat: {coords['latitude']}")
                        st.write(f"Lng: {coords['longitude']}")
                
                with col2:
                    if "map_html" in location_info:
                        st.markdown("**Map Location:**")
                        st.components.v1.html(location_info["map_html"], height=450)
        
        except Exception as e:
            st.info(f"Map display not available: {str(e)}")


def main():
    """Main application function."""
    initialize_session_state()
    display_header()
    provider, model = display_sidebar()
    
    # Check API keys
    issues = check_api_keys()
    if any("❌" in issue for issue in issues):
        st.error("Critical API keys missing! Please configure your .env file.")
        st.info("Copy .env.example to .env and add your API keys.")
        st.code("cp .env.example .env", language="bash")
        return
    
    # Initialize agent
    try:
        if st.session_state.agent is None:
            with st.spinner("Initializing agent..."):
                st.session_state.agent = create_financial_agent(
                    model_name=model,
                    provider=provider
                )
            st.success("Agent initialized successfully!")
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return
    
    # Sample queries
    display_sample_queries()
    
    st.markdown("---")
    
    # Main input
    st.markdown('<div class="section-header">🔍 Query</div>', unsafe_allow_html=True)
    
    # Get country input
    default_country = st.session_state.get('selected_country', '')
    country_input = st.text_input(
        "Enter country name:",
        value=default_country,
        placeholder="e.g., Japan, India, United States",
        help="Enter the name of the country you want financial information for"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        submit_button = st.button("🚀 Get Financial Details", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.results = None
        st.session_state.map_location = None
        if 'selected_country' in st.session_state:
            del st.session_state.selected_country
        st.rerun()
    
    # Process query
    if submit_button and country_input:
        if 'selected_country' in st.session_state:
            del st.session_state.selected_country
        
        with st.spinner(f"🔄 Fetching financial information for {country_input}..."):
            try:
                result = st.session_state.agent.get_financial_info(country_input)
                st.session_state.results = result
                
                if result["success"]:
                    st.balloons()
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.results = None
    
    # Display results
    if st.session_state.results and st.session_state.results.get("success"):
        parse_and_display_results(
            st.session_state.results["output"],
            country_input
        )
    
    elif st.session_state.results and not st.session_state.results.get("success"):
        st.markdown('<div class="error-box">❌ Failed to fetch information. Please check your API keys and try again.</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
