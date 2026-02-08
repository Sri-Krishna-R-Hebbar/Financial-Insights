"""
Google Maps Tools for displaying stock exchange locations.
Real-time location data via Google Maps Embed API.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class GoogleMapsMCPTool:
    """MCP-compliant tool for Google Maps integration."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        
        # Stock exchange headquarters coordinates
        self.exchange_locations = {
            "Tokyo Stock Exchange": {
                "address": "Tokyo Stock Exchange, 2-1 Nihonbashi-Kabutocho, Chuo City, Tokyo, Japan",
                "lat": 35.6809,
                "lng": 139.7776,
                "query": "Tokyo Stock Exchange"
            },
            "National Stock Exchange of India": {
                "address": "Exchange Plaza, Bandra Kurla Complex, Bandra East, Mumbai, Maharashtra 400051, India",
                "lat": 19.0633,
                "lng": 72.8706,
                "query": "National Stock Exchange of India, Mumbai"
            },
            "New York Stock Exchange": {
                "address": "11 Wall St, New York, NY 10005, United States",
                "lat": 40.7074,
                "lng": -74.0113,
                "query": "New York Stock Exchange"
            },
            "London Stock Exchange": {
                "address": "10 Paternoster Square, London EC4M 7LS, United Kingdom",
                "lat": 51.5142,
                "lng": -0.0991,
                "query": "London Stock Exchange"
            },
            "Korea Exchange": {
                "address": "76 Yeouinaru-ro, Yeongdeungpo-gu, Seoul, South Korea",
                "lat": 37.5262,
                "lng": 126.9282,
                "query": "Korea Exchange, Seoul"
            },
            "Shanghai Stock Exchange": {
                "address": "528 Pudong South Road, Pudong, Shanghai, China",
                "lat": 31.2385,
                "lng": 121.5007,
                "query": "Shanghai Stock Exchange"
            },
            "Frankfurt Stock Exchange": {
                "address": "Börsenplatz 4, 60313 Frankfurt am Main, Germany",
                "lat": 50.1135,
                "lng": 8.6762,
                "query": "Frankfurt Stock Exchange"
            },
            "Euronext Paris": {
                "address": "39 Rue Cambon, 75001 Paris, France",
                "lat": 48.8675,
                "lng": 2.3265,
                "query": "Euronext Paris"
            },
            "Toronto Stock Exchange": {
                "address": "The Exchange Tower, 130 King St W, Toronto, ON M5X 1J2, Canada",
                "lat": 43.6478,
                "lng": -79.3813,
                "query": "Toronto Stock Exchange"
            },
            "Australian Securities Exchange": {
                "address": "20 Bridge St, Sydney NSW 2000, Australia",
                "lat": -33.8646,
                "lng": 151.2101,
                "query": "Australian Securities Exchange, Sydney"
            },
            "Hong Kong Stock Exchange": {
                "address": "8 Finance St, Central, Hong Kong",
                "lat": 22.2845,
                "lng": 114.1580,
                "query": "Hong Kong Stock Exchange"
            },
            "Singapore Exchange": {
                "address": "2 Shenton Way, Singapore 068804",
                "lat": 1.2789,
                "lng": 103.8497,
                "query": "Singapore Exchange"
            },
            "B3 - Brasil Bolsa Balcão": {
                "address": "Praça Antonio Prado, 48 - Centro Histórico de São Paulo, São Paulo, Brazil",
                "lat": -23.5449,
                "lng": -46.6342,
                "query": "B3 Stock Exchange, São Paulo"
            },
            "SIX Swiss Exchange": {
                "address": "Pfingstweidstrasse 110, 8005 Zürich, Switzerland",
                "lat": 47.3897,
                "lng": 8.5162,
                "query": "SIX Swiss Exchange, Zurich"
            },
            "Bolsa de Madrid": {
                "address": "Plaza de la Lealtad, 1, 28014 Madrid, Spain",
                "lat": 40.4169,
                "lng": -3.6943,
                "query": "Bolsa de Madrid"
            },
            "Borsa Italiana": {
                "address": "Piazza Affari, 6, 20123 Milano MI, Italy",
                "lat": 45.4654,
                "lng": 9.1859,
                "query": "Borsa Italiana, Milan"
            },
            "Euronext Amsterdam": {
                "address": "Beursplein 5, 1012 JW Amsterdam, Netherlands",
                "lat": 52.3736,
                "lng": 4.8936,
                "query": "Euronext Amsterdam"
            },
            "Nasdaq Stockholm": {
                "address": "Tullvaktsvägen 15, 115 56 Stockholm, Sweden",
                "lat": 59.3326,
                "lng": 18.0824,
                "query": "Nasdaq Stockholm"
            },
            "Moscow Exchange": {
                "address": "13 Bolshoy Kislovsky Lane, Moscow, Russia",
                "lat": 55.7595,
                "lng": 37.6028,
                "query": "Moscow Exchange"
            },
            "Mexican Stock Exchange": {
                "address": "Paseo de la Reforma 255, Cuauhtémoc, Mexico City, Mexico",
                "lat": 19.4284,
                "lng": -99.1677,
                "query": "Mexican Stock Exchange, Mexico City"
            },
            "Stock Exchange of Thailand": {
                "address": "93 Ratchadaphisek Road, Din Daeng, Bangkok, Thailand",
                "lat": 13.7649,
                "lng": 100.5630,
                "query": "Stock Exchange of Thailand, Bangkok"
            },
            "Indonesia Stock Exchange": {
                "address": "Jl. Jend. Sudirman Kav 52-53, Jakarta 12190, Indonesia",
                "lat": -6.2258,
                "lng": 106.8086,
                "query": "Indonesia Stock Exchange, Jakarta"
            },
            "Bursa Malaysia": {
                "address": "15 Jalan Semantan, Bukit Damansara, 50490 Kuala Lumpur, Malaysia",
                "lat": 3.1520,
                "lng": 101.6695,
                "query": "Bursa Malaysia, Kuala Lumpur"
            },
        }
    
    def get_embed_url(self, exchange_name: str) -> str:
        """
        Generate Google Maps embed URL for a stock exchange.
        
        Args:
            exchange_name: Name of the stock exchange
            
        Returns:
            Google Maps embed URL
        """
        if not self.api_key:
            return ""
        
        location = self.exchange_locations.get(exchange_name)
        
        if not location:
            # Fallback: try to search by name
            query = exchange_name.replace(" ", "+")
            return f"https://www.google.com/maps/embed/v1/place?key={self.api_key}&q={query}"
        
        # Use place mode with query
        query = location["query"].replace(" ", "+")
        embed_url = f"https://www.google.com/maps/embed/v1/place?key={self.api_key}&q={query}&zoom=15"
        
        return embed_url
    
    def get_map_html(self, exchange_name: str, width: int = 600, height: int = 450) -> str:
        """
        Generate HTML iframe for embedding Google Maps.
        
        Args:
            exchange_name: Name of the stock exchange
            width: Width of the map in pixels
            height: Height of the map in pixels
            
        Returns:
            HTML iframe code
        """
        embed_url = self.get_embed_url(exchange_name)
        
        if not embed_url:
            return "<p>Google Maps API key not configured</p>"
        
        html = f'''
        <iframe
            width="{width}"
            height="{height}"
            style="border:0"
            loading="lazy"
            allowfullscreen
            referrerpolicy="no-referrer-when-downgrade"
            src="{embed_url}">
        </iframe>
        '''
        
        return html
    
    def get_location_info(self, exchange_name: str) -> Dict[str, Any]:
        """
        Get location information for a stock exchange.
        
        Args:
            exchange_name: Name of the stock exchange
            
        Returns:
            Dict with location details and map URL
        """
        location = self.exchange_locations.get(exchange_name)
        
        if not location:
            return {
                "exchange": exchange_name,
                "error": "Location information not available",
                "map_url": self.get_embed_url(exchange_name)
            }
        
        return {
            "exchange": exchange_name,
            "address": location["address"],
            "coordinates": {
                "latitude": location["lat"],
                "longitude": location["lng"]
            },
            "map_url": self.get_embed_url(exchange_name),
            "map_html": self.get_map_html(exchange_name)
        }


# Standalone function for LangChain tool
def get_exchange_location(exchange_name: str) -> Dict[str, Any]:
    """
    Get Google Maps location for a stock exchange.
    
    Args:
        exchange_name: Name of the primary stock exchange
        
    Returns:
        Dict with location info and map embed URL
    """
    tool = GoogleMapsMCPTool()
    return tool.get_location_info(exchange_name)
