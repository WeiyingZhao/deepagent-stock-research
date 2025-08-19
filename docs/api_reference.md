# API Reference

## Core Components

### DeepAgent Creation

```python
from deepagents import create_deep_agent
from langchain_ollama import ChatOllama

# Create the agent
agent = create_deep_agent(
    tools=tools_list,
    instructions=research_instructions,
    subagents=subagents_list,
    model=model
)
```

### Model Configuration

```python
from langchain_ollama import ChatOllama

# Basic model setup
model = ChatOllama(
    model="gpt-oss",
    temperature=0,
    top_p=0.9,
    max_tokens=2048
)
```

## Built-in Tools

### get_stock_price(symbol: str)

Retrieves current stock price and basic company information.

**Parameters:**
- `symbol` (str): Stock ticker symbol (e.g., "AAPL", "MSFT")

**Returns:**
- JSON string containing:
  - `symbol`: Stock ticker
  - `current_price`: Current trading price
  - `company_name`: Full company name
  - `market_cap`: Market capitalization
  - `pe_ratio`: Price-to-earnings ratio
  - `52_week_high`: 52-week high price
  - `52_week_low`: 52-week low price

**Example:**
```python
result = get_stock_price("AAPL")
# Returns: {"symbol": "AAPL", "current_price": 184.12, ...}
```

### get_financial_statements(symbol: str)

Retrieves key financial statement data from the most recent annual report.

**Parameters:**
- `symbol` (str): Stock ticker symbol

**Returns:**
- JSON string containing:
  - `symbol`: Stock ticker
  - `period`: Financial year
  - `revenue`: Total revenue
  - `net_income`: Net income
  - `total_assets`: Total assets
  - `total_debt`: Total debt

**Example:**
```python
result = get_financial_statements("AAPL")
# Returns: {"symbol": "AAPL", "period": "2024", "revenue": 385700000000, ...}
```

### get_technical_indicators(symbol: str, period: str = "3mo")

Calculates technical indicators for the specified stock.

**Parameters:**
- `symbol` (str): Stock ticker symbol
- `period` (str): Historical period ("1mo", "3mo", "6mo", "1y", "2y", "5y")

**Returns:**
- JSON string containing:
  - `symbol`: Stock ticker
  - `current_price`: Current price
  - `sma_20`: 20-day Simple Moving Average
  - `sma_50`: 50-day Simple Moving Average
  - `rsi`: Relative Strength Index (14-day)
  - `volume`: Current volume
  - `trend_signal`: "bullish" or "bearish"

**Example:**
```python
result = get_technical_indicators("AAPL", "6mo")
# Returns: {"symbol": "AAPL", "current_price": 184.12, "rsi": 62.3, ...}
```

## Custom Tools

### get_company_news(symbol: str, limit: int = 5)

Fetches recent news articles for a company.

**Parameters:**
- `symbol` (str): Stock ticker symbol
- `limit` (int): Number of articles to retrieve

**Returns:**
- JSON with news articles, headlines, sentiment analysis

### calculate_intrinsic_value(symbol: str, growth_rate: float = 0.05)

Calculates intrinsic value using DCF model.

**Parameters:**
- `symbol` (str): Stock ticker symbol
- `growth_rate` (float): Expected growth rate (default: 5%)

**Returns:**
- JSON with DCF valuation, intrinsic value, and recommendation

### get_insider_trading(symbol: str)

Retrieves insider trading activity.

**Parameters:**
- `symbol` (str): Stock ticker symbol

**Returns:**
- JSON with recent insider transactions and net activity

### analyze_options_flow(symbol: str)

Analyzes options flow and unusual activity.

**Parameters:**
- `symbol` (str): Stock ticker symbol

**Returns:**
- JSON with options volume, unusual activity, and sentiment

## Sub-Agents

### Fundamental Analyst

Specializes in financial statement analysis and valuation.

**Configuration:**
```python
fundamental_analyst = {
    "name": "fundamental-analyst",
    "description": "Performs deep fundamental analysis",
    "prompt": "Expert fundamental analyst with 15+ years experience..."
}
```

**Focus Areas:**
- Financial ratios (P/E, P/B, ROE, ROA)
- Growth metrics and trends
- Industry comparisons
- Intrinsic value calculations

### Technical Analyst

Specializes in chart analysis and trading signals.

**Configuration:**
```python
technical_analyst = {
    "name": "technical-analyst",
    "description": "Analyzes price patterns and technical indicators",
    "prompt": "Professional technical analyst specializing in chart analysis..."
}
```

**Focus Areas:**
- Price action and trend analysis
- Technical indicators (RSI, MACD, Moving Averages)
- Support and resistance levels
- Entry/exit recommendations

### Risk Analyst

Evaluates investment risks and provides risk assessment.

**Configuration:**
```python
risk_analyst = {
    "name": "risk-analyst",
    "description": "Evaluates investment risks",
    "prompt": "Risk management specialist focused on identifying risks..."
}
```

**Focus Areas:**
- Market risk analysis
- Company-specific risks
- Sector and industry risks
- Regulatory and compliance risks

## Agent Invocation

### Basic Usage

```python
# Simple query
result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze Apple Inc. (AAPL)"}]
})

# Extract response
response = result["messages"][-1]["content"]
```

### Advanced Usage

```python
# Complex multi-part query
query = """
Conduct comprehensive analysis of Tesla (TSLA) including:
1. Fundamental analysis with DCF valuation
2. Technical analysis with entry points
3. Risk assessment including regulatory risks
4. ESG evaluation
5. 12-month price target with confidence intervals
"""

result = agent.invoke({
    "messages": [{"role": "user", "content": query}]
})
```

### Error Handling

```python
try:
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    # Process result
    if "messages" in result and result["messages"]:
        response = result["messages"][-1]["content"]
    else:
        response = "No response received"
        
except Exception as e:
    response = f"Error: {str(e)}"
```

## Custom Sub-Agent Creation

### Creating a New Sub-Agent

```python
custom_subagent = {
    "name": "esg-analyst",
    "description": "ESG specialist for sustainable investing analysis",
    "prompt": """You are an ESG expert with deep knowledge of:
    - Environmental impact assessment
    - Social responsibility metrics  
    - Corporate governance evaluation
    - Sustainability reporting standards
    
    Always provide specific ESG scores and framework references."""
}
```

### Adding to Agent

```python
# Combine with existing sub-agents
all_subagents = [
    fundamental_analyst,
    technical_analyst, 
    risk_analyst,
    custom_subagent
]

# Create enhanced agent
enhanced_agent = create_deep_agent(
    tools=tools,
    instructions=instructions,
    subagents=all_subagents,
    model=model
)
```

## Configuration Management

### Using Configuration Files

```python
# Import configurations
from config.model_config import create_ollama_model
from config.custom_tools import CUSTOM_TOOLS
from config.custom_subagents import CUSTOM_SUBAGENTS

# Create configured agent
model = create_ollama_model("analytical")
tools = base_tools + CUSTOM_TOOLS
subagents = default_subagents + CUSTOM_SUBAGENTS[:2]

agent = create_deep_agent(
    tools=tools,
    instructions=instructions,
    subagents=subagents,
    model=model
)
```

### Environment Variables

```python
import os

# Model configuration from environment
model_name = os.getenv("OLLAMA_MODEL", "gpt-oss")
temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0"))

model = ChatOllama(
    model=model_name,
    temperature=temperature
)
```

## Best Practices

1. **Error Handling**: Always wrap agent calls in try-catch blocks
2. **Response Validation**: Check for valid response structure
3. **Rate Limiting**: Implement delays for multiple API calls
4. **Logging**: Enable logging for debugging and monitoring
5. **Resource Management**: Clean up resources after use

## Examples

See the [examples directory](../examples/) for complete working examples:
- `integration_examples.py`: Advanced integration patterns
- `sample_queries.md`: Example queries and use cases
- `sample_output.txt`: Expected output format