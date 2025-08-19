# Best Practices Guide

## Project Structure and Organization

### Recommended Directory Layout
```
deepagent-stock-research/
├── research_agent.py          # Main application
├── requirements.txt           # Dependencies
├── CLAUDE.md                 # Claude Code guidance
├── README.md                 # Project documentation
├── config/                   # Configuration files
│   ├── model_config.py       # Model configurations
│   ├── custom_tools.py       # Custom tool definitions
│   └── custom_subagents.py   # Custom sub-agent configs
├── examples/                 # Usage examples
│   ├── sample_queries.md     # Example queries
│   ├── sample_output.txt     # Expected outputs
│   └── integration_examples.py # Integration patterns
├── docs/                     # Documentation
│   ├── installation.md       # Setup instructions
│   ├── api_reference.md      # API documentation
│   ├── troubleshooting.md    # Common issues
│   └── best_practices.md     # This file
└── screenshots/              # Project screenshots
```

## Development Best Practices

### 1. Code Organization

#### Modular Design
```python
# Good: Separate concerns
from config.model_config import create_ollama_model
from config.custom_tools import CUSTOM_TOOLS
from config.custom_subagents import CUSTOM_SUBAGENTS

# Avoid: Everything in one large file
```

#### Tool Development
```python
# Good: Comprehensive error handling
@tool
def get_stock_price(symbol: str) -> str:
    """Get current stock price with comprehensive error handling."""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Validate data availability
        if not info or 'regularMarketPrice' not in info:
            return json.dumps({"error": f"No data available for {symbol}"})
            
        # Return structured data
        return json.dumps({
            "symbol": symbol,
            "price": info.get('regularMarketPrice'),
            "currency": info.get('currency', 'USD'),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error fetching {symbol}: {e}")
        return json.dumps({"error": str(e)})

# Avoid: Minimal error handling
@tool 
def bad_stock_price(symbol: str) -> str:
    stock = yf.Ticker(symbol)
    return str(stock.info['regularMarketPrice'])  # Will crash on missing data
```

#### Sub-Agent Configuration
```python
# Good: Detailed, specific prompts
analyst = {
    "name": "fundamental-analyst",
    "description": "Comprehensive fundamental analysis specialist",
    "prompt": """You are a CFA-certified fundamental analyst with 15+ years experience.
    
    Your analysis must include:
    - P/E, P/B, ROE, ROA, Debt-to-Equity ratios
    - 5-year historical growth trends
    - Industry peer comparisons
    - DCF valuation with explicit assumptions
    
    Always cite specific numbers and provide methodology."""
}

# Avoid: Vague prompts
bad_analyst = {
    "name": "analyst",
    "description": "Does analysis",
    "prompt": "You analyze stocks."
}
```

### 2. Data Quality and Validation

#### Input Validation
```python
import re

def validate_stock_symbol(symbol: str) -> bool:
    """Validate stock symbol format."""
    if not symbol or len(symbol) > 5:
        return False
    return re.match(r'^[A-Z]{1,5}$', symbol.upper()) is not None

def sanitize_input(query: str) -> str:
    """Sanitize user input for safe processing."""
    # Remove potentially dangerous characters
    cleaned = re.sub(r'[<>\"\'&]', '', query)
    return cleaned.strip()
```

#### Data Source Reliability
```python
def get_reliable_stock_data(symbol: str, max_retries: int = 3):
    """Get stock data with retry logic and fallback sources."""
    
    for attempt in range(max_retries):
        try:
            # Primary source: yfinance
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            
            if not data.empty:
                return data
                
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # Brief delay before retry
    
    # Fallback: Return cached data or error
    return get_cached_data(symbol) or {"error": "Data unavailable"}
```

### 3. Performance Optimization

#### Caching Strategy
```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def cached_stock_data(symbol: str, cache_duration: int = 300):
    """Cache stock data for 5 minutes to reduce API calls."""
    timestamp = int(time.time())
    cache_key = f"{symbol}_{timestamp // cache_duration}"
    
    # Implementation would include actual caching logic
    return get_stock_data_internal(symbol)
```

#### Async Processing for Multiple Stocks
```python
import asyncio
import aiohttp

async def get_multiple_stocks(symbols: list) -> dict:
    """Fetch multiple stocks concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [get_stock_async(session, symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
    return dict(zip(symbols, results))
```

#### Model Optimization
```python
# Good: Optimize for specific use case
creative_model = ChatOllama(
    model="gpt-oss",
    temperature=0.7,       # Higher for creative analysis
    max_tokens=1024,       # Reasonable limit
    top_p=0.9,            # Nucleus sampling
    frequency_penalty=0.1  # Reduce repetition
)

analytical_model = ChatOllama(
    model="gpt-oss", 
    temperature=0.1,       # Lower for analytical work
    max_tokens=2048,       # More detail needed
    top_p=0.8,            # More focused
    frequency_penalty=0.0  # Precision over creativity
)
```

### 4. Security Best Practices

#### API Key Management
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Good: Use environment variables
API_KEY = os.getenv('FINANCIAL_API_KEY')
if not API_KEY:
    raise ValueError("FINANCIAL_API_KEY environment variable required")

# Avoid: Hardcoded keys
# API_KEY = "sk-1234567890"  # NEVER DO THIS
```

#### Input Sanitization
```python
def safe_sql_query(symbol: str) -> str:
    """Demonstrate safe query construction."""
    # Whitelist approach
    if not re.match(r'^[A-Z0-9]{1,5}$', symbol):
        raise ValueError("Invalid symbol format")
    
    # Use parameterized queries
    query = "SELECT * FROM stocks WHERE symbol = %s"
    return query, (symbol,)
```

#### Rate Limiting
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_calls: int = 10, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        now = time.time()
        # Clean old calls
        self.calls[identifier] = [
            call_time for call_time in self.calls[identifier]
            if now - call_time < self.time_window
        ]
        
        if len(self.calls[identifier]) >= self.max_calls:
            return False
            
        self.calls[identifier].append(now)
        return True

# Usage
limiter = RateLimiter(max_calls=5, time_window=60)
if not limiter.is_allowed(user_id):
    return "Rate limit exceeded. Please wait."
```

### 5. Error Handling and Logging

#### Comprehensive Error Handling
```python
import logging
from typing import Optional, Dict, Any

def robust_analysis(symbol: str) -> Dict[str, Any]:
    """Perform analysis with comprehensive error handling."""
    
    try:
        # Validate input
        if not validate_stock_symbol(symbol):
            return {"error": "Invalid stock symbol", "code": "INVALID_INPUT"}
        
        # Attempt analysis
        result = perform_stock_analysis(symbol)
        
        # Validate output
        if not result or 'price' not in result:
            return {"error": "Incomplete data received", "code": "DATA_INCOMPLETE"}
            
        return {"success": True, "data": result}
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error for {symbol}: {e}")
        return {"error": "Network connectivity issue", "code": "NETWORK_ERROR"}
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error for {symbol}: {e}")
        return {"error": "Data format error", "code": "PARSE_ERROR"}
        
    except Exception as e:
        logging.exception(f"Unexpected error analyzing {symbol}")
        return {"error": "Internal error occurred", "code": "INTERNAL_ERROR"}
```

#### Structured Logging
```python
import logging
import json

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_analysis(self, symbol: str, duration: float, success: bool, **kwargs):
        log_data = {
            "timestamp": time.time(),
            "symbol": symbol,
            "duration_ms": duration * 1000,
            "success": success,
            **kwargs
        }
        self.logger.info(json.dumps(log_data))

# Usage
logger = StructuredLogger("stock_analysis")
start_time = time.time()
# ... perform analysis ...
logger.log_analysis(symbol, time.time() - start_time, True, result_length=len(result))
```

### 6. Testing and Quality Assurance

#### Unit Testing
```python
import unittest
from unittest.mock import patch, MagicMock

class TestStockTools(unittest.TestCase):
    
    @patch('yfinance.Ticker')
    def test_get_stock_price_success(self, mock_ticker):
        # Setup mock
        mock_ticker.return_value.info = {
            'regularMarketPrice': 150.0,
            'longName': 'Apple Inc.'
        }
        
        # Test
        result = get_stock_price('AAPL')
        data = json.loads(result)
        
        # Assertions
        self.assertEqual(data['symbol'], 'AAPL')
        self.assertEqual(data['current_price'], 150.0)
    
    @patch('yfinance.Ticker')
    def test_get_stock_price_failure(self, mock_ticker):
        # Setup mock to raise exception
        mock_ticker.side_effect = Exception("Network error")
        
        # Test
        result = get_stock_price('INVALID')
        data = json.loads(result)
        
        # Assertions
        self.assertIn('error', data)
```

#### Integration Testing
```python
def integration_test_full_analysis():
    """Test complete analysis workflow."""
    
    # Test with known good symbol
    query = "Analyze Apple Inc. (AAPL) briefly"
    
    try:
        result = run_stock_research(query)
        
        # Verify response structure
        assert len(result) > 100, "Response too short"
        assert "AAPL" in result, "Symbol not found in response"
        assert any(word in result.lower() for word in ['buy', 'sell', 'hold']), "No recommendation found"
        
        print("✓ Integration test passed")
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
```

### 7. Documentation Standards

#### Code Documentation
```python
def get_financial_ratios(symbol: str, period: str = "annual") -> Dict[str, float]:
    """
    Calculate key financial ratios for a stock.
    
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        period (str): Time period for calculations ('annual' or 'quarterly')
        
    Returns:
        Dict[str, float]: Dictionary containing calculated ratios:
            - pe_ratio: Price-to-earnings ratio
            - pb_ratio: Price-to-book ratio
            - roe: Return on equity
            - roa: Return on assets
            - debt_to_equity: Debt-to-equity ratio
            
    Raises:
        ValueError: If symbol is invalid or data unavailable
        ConnectionError: If unable to fetch financial data
        
    Example:
        >>> ratios = get_financial_ratios('AAPL')
        >>> print(f"P/E Ratio: {ratios['pe_ratio']:.2f}")
        P/E Ratio: 28.50
    """
    # Implementation here
```

#### README Updates
Keep README.md current with:
- Latest feature additions
- Updated installation instructions
- New configuration options
- Recent example outputs

### 8. Production Deployment

#### Environment Configuration
```python
# config/production.py
import os

class ProductionConfig:
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    GRADIO_HOST = os.getenv('GRADIO_HOST', '0.0.0.0')
    GRADIO_PORT = int(os.getenv('GRADIO_PORT', 7860))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', 10))
    CACHE_TTL = int(os.getenv('CACHE_TTL', 300))  # 5 minutes
```

#### Health Checks
```python
def health_check() -> Dict[str, Any]:
    """System health check for monitoring."""
    
    checks = {
        "ollama": check_ollama_connection(),
        "yfinance": check_data_source(),
        "memory": check_memory_usage(),
        "disk": check_disk_space()
    }
    
    overall_status = all(checks.values())
    
    return {
        "status": "healthy" if overall_status else "unhealthy",
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }
```

### 9. Monitoring and Observability

#### Metrics Collection
```python
import time
from collections import Counter, defaultdict

class MetricsCollector:
    def __init__(self):
        self.request_count = Counter()
        self.response_times = defaultdict(list)
        self.error_count = Counter()
    
    def record_request(self, endpoint: str, duration: float, success: bool):
        self.request_count[endpoint] += 1
        self.response_times[endpoint].append(duration)
        
        if not success:
            self.error_count[endpoint] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        return {
            "total_requests": sum(self.request_count.values()),
            "avg_response_time": {
                endpoint: sum(times) / len(times)
                for endpoint, times in self.response_times.items()
            },
            "error_rate": {
                endpoint: self.error_count[endpoint] / self.request_count[endpoint]
                for endpoint in self.request_count
            }
        }
```

## Quality Gates

### Pre-Deployment Checklist

- [ ] All unit tests passing
- [ ] Integration tests successful
- [ ] Security scan completed
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Error handling verified
- [ ] Logging configured
- [ ] Monitoring setup
- [ ] Backup strategy in place
- [ ] Rollback plan prepared

### Code Review Guidelines

1. **Functionality**: Does the code work as intended?
2. **Security**: Are there any security vulnerabilities?
3. **Performance**: Will this impact system performance?
4. **Maintainability**: Is the code easy to understand and modify?
5. **Testing**: Are appropriate tests included?
6. **Documentation**: Is the code properly documented?

Remember: Quality is everyone's responsibility. These practices ensure the DeepAgent Stock Research system remains reliable, secure, and maintainable.