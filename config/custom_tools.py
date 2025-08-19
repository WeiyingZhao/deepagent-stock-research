"""
Custom Tools Configuration
Examples of how to create and add custom analysis tools
"""

from langchain_core.tools import tool
import requests
import json
from typing import Dict, List
import yfinance as yf

@tool
def get_company_news(symbol: str, limit: int = 5) -> str:
    """Fetch recent news articles for a company."""
    try:
        # This is a placeholder - you would integrate with a real news API
        # Example: Alpha Vantage, NewsAPI, or similar service
        
        # Simulated news data structure
        news_data = {
            "symbol": symbol,
            "articles": [
                {
                    "headline": f"Sample news article for {symbol}",
                    "summary": f"Recent developments in {symbol} show...",
                    "sentiment": "neutral",
                    "date": "2024-01-15"
                }
            ]
        }
        
        return json.dumps(news_data, indent=2)
    except Exception as e:
        return f"Error fetching news: {str(e)}"

@tool
def calculate_intrinsic_value(symbol: str, growth_rate: float = 0.05) -> str:
    """Calculate intrinsic value using DCF model."""
    try:
        # This would integrate with financial data to perform DCF calculation
        # Placeholder implementation
        
        result = {
            "symbol": symbol,
            "method": "DCF",
            "growth_rate": growth_rate,
            "intrinsic_value": 150.00,  # Calculated value
            "current_price": 140.00,    # From market data
            "upside_potential": "7.1%",
            "recommendation": "BUY" if 150.00 > 140.00 else "SELL"
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error calculating intrinsic value: {str(e)}"

@tool
def get_insider_trading(symbol: str) -> str:
    """Get insider trading activity for a stock."""
    try:
        # Placeholder for insider trading data
        insider_data = {
            "symbol": symbol,
            "recent_transactions": [
                {
                    "insider": "CEO John Doe",
                    "transaction": "BUY",
                    "shares": 10000,
                    "price": 138.50,
                    "date": "2024-01-10"
                }
            ],
            "net_insider_activity": "POSITIVE"
        }
        
        return json.dumps(insider_data, indent=2)
    except Exception as e:
        return f"Error fetching insider trading: {str(e)}"

@tool
def analyze_options_flow(symbol: str) -> str:
    """Analyze options flow and unusual activity."""
    try:
        options_data = {
            "symbol": symbol,
            "unusual_activity": {
                "call_volume": 15000,
                "put_volume": 8000,
                "call_put_ratio": 1.875,
                "large_trades": [
                    {
                        "type": "CALL",
                        "strike": 150,
                        "expiry": "2024-02-16",
                        "volume": 5000,
                        "sentiment": "BULLISH"
                    }
                ]
            },
            "sentiment": "BULLISH"
        }
        
        return json.dumps(options_data, indent=2)
    except Exception as e:
        return f"Error analyzing options flow: {str(e)}"

# List of all custom tools
CUSTOM_TOOLS = [
    get_company_news,
    calculate_intrinsic_value,
    get_insider_trading,
    analyze_options_flow
]

# Tool categories for organization
TOOL_CATEGORIES = {
    "fundamental": [calculate_intrinsic_value],
    "sentiment": [get_company_news, get_insider_trading],
    "technical": [analyze_options_flow],
    "all": CUSTOM_TOOLS
}

def get_tools_by_category(category: str = "all") -> List:
    """Get tools by category."""
    return TOOL_CATEGORIES.get(category, CUSTOM_TOOLS)