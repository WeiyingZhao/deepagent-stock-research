# Detailed Usage Examples

## Table of Contents
1. [Basic Analysis Examples](#basic-analysis-examples)
2. [Advanced Analysis Examples](#advanced-analysis-examples)
3. [Custom Configuration Examples](#custom-configuration-examples)
4. [Programmatic Usage Examples](#programmatic-usage-examples)
5. [Integration Examples](#integration-examples)
6. [Real-World Scenarios](#real-world-scenarios)

## Basic Analysis Examples

### Example 1: Simple Stock Analysis

**Query:**
```
Analyze Apple Inc. (AAPL)
```

**What it does:**
- Fetches current stock price and basic metrics
- Performs fundamental analysis using financial statements
- Conducts technical analysis with indicators
- Provides risk assessment
- Gives buy/hold/sell recommendation

**Expected Output Structure:**
```
=== STOCK ANALYSIS REPORT ===
Company: Apple Inc. (AAPL)
Current Price: $184.12
Recommendation: BUY
Target Price: $210.00

FUNDAMENTAL ANALYSIS
- P/E Ratio: 28.5x
- Revenue Growth: 1.3% YoY
- ROE: 147.4%
[detailed metrics...]

TECHNICAL ANALYSIS  
- Trend: BULLISH
- RSI: 62.3 (Neutral-Bullish)
- Support: $175, Resistance: $195
[detailed indicators...]

RISK ASSESSMENT
- Overall Risk: MODERATE
- Key Risks: Market volatility, regulatory concerns
[detailed risk analysis...]
```

### Example 2: Comprehensive Investment Analysis

**Query:**
```
Conduct a comprehensive analysis of Tesla (TSLA) for a 6-month investment horizon. Include:
1. Financial performance and valuation
2. Technical analysis with entry points
3. Risk assessment including regulatory risks
4. Price target with confidence intervals
```

**What it does:**
- Performs all analysis types with specific focus on 6-month timeframe
- Provides detailed valuation metrics
- Identifies optimal entry points
- Assesses regulatory risks specific to Tesla
- Gives price targets with confidence levels

### Example 3: Quick Screening Query

**Query:**
```
Is Microsoft (MSFT) a good buy right now? Keep it brief.
```

**What it does:**
- Provides concise analysis focusing on current investment merit
- Quick fundamental and technical check
- Simple buy/hold/sell recommendation
- Brief reasoning for the recommendation

## Advanced Analysis Examples

### Example 4: Multi-Stock Comparison

**Query:**
```
Compare Apple (AAPL), Microsoft (MSFT), and Google (GOOGL) for a technology-focused portfolio. 
Analyze:
- Relative valuation metrics
- Growth prospects
- Risk profiles
- Recommended allocation percentages
- Portfolio diversification benefits
```

**What it does:**
- Analyzes each stock individually
- Compares key metrics across all three
- Evaluates correlation and diversification
- Provides portfolio allocation recommendations
- Assesses combined risk profile

### Example 5: Sector Analysis

**Query:**
```
Analyze the semiconductor sector outlook for Q1 2025. Focus on:
- Industry trends and drivers
- Key players: NVIDIA (NVDA), AMD (AMD), Intel (INTC)
- Supply chain considerations
- Investment opportunities and risks
- Sector rotation implications
```

**What it does:**
- Evaluates sector-wide trends and catalysts
- Compares major sector players
- Assesses supply chain impacts
- Identifies sector-specific opportunities
- Considers macro factors affecting the sector

### Example 6: ESG-Focused Analysis

**Query:**
```
Evaluate Tesla (TSLA) from an ESG (Environmental, Social, Governance) perspective:
- Environmental impact and sustainability initiatives
- Social responsibility and labor practices
- Corporate governance structure
- ESG scores and ratings
- Impact on investment thesis and valuation
```

**What it does:**
- Analyzes environmental initiatives and impact
- Evaluates social responsibility programs
- Assesses governance structure and practices
- Integrates ESG factors into investment recommendation
- Considers ESG trends and investor preferences

### Example 7: Crisis/Event Analysis

**Query:**
```
Assess the impact of recent supply chain disruptions on Apple (AAPL):
- Supply chain vulnerability analysis
- Revenue and margin impact assessment
- Management response evaluation
- Recovery timeline estimation
- Investment implications and opportunities
```

**What it does:**
- Analyzes specific event impact on business
- Evaluates management response and adaptation
- Assesses financial impact and recovery prospects
- Provides event-driven investment insights
- Considers both risks and opportunities

## Custom Configuration Examples

### Example 8: Using Enhanced Agent with Custom Tools

**Python Code:**
```python
from examples.integration_examples import create_enhanced_research_agent

# Create enhanced agent with all custom tools and sub-agents
enhanced_agent = create_enhanced_research_agent()

# Query with enhanced capabilities
query = """
Analyze Netflix (NFLX) using all available analysis tools:
- Include news sentiment analysis
- Calculate intrinsic value using DCF
- Analyze insider trading activity
- Evaluate options flow and sentiment
- Provide ESG assessment
- Include sector comparison
"""

result = enhanced_agent.invoke({
    "messages": [{"role": "user", "content": query}]
})

print(result["messages"][-1]["content"])
```

### Example 9: Specialized ESG Agent

**Python Code:**
```python
from examples.integration_examples import create_specialized_research_agent

# Create ESG-focused agent
esg_agent = create_specialized_research_agent(focus="esg")

query = """
Evaluate the top 5 ESG technology stocks:
- Microsoft (MSFT)
- Apple (AAPL) 
- Alphabet (GOOGL)
- Adobe (ADBE)
- Salesforce (CRM)

Rank them by ESG performance and provide investment recommendations.
"""

result = esg_agent.invoke({
    "messages": [{"role": "user", "content": query}]
})
```

### Example 10: Quantitative Analysis Agent

**Python Code:**
```python
# Create quant-focused agent
quant_agent = create_specialized_research_agent(focus="quantitative")

query = """
Perform quantitative analysis on Amazon (AMZN):
- Statistical backtesting of price patterns
- Volatility analysis and correlation studies
- Factor model analysis
- Monte Carlo simulation for price targets
- Risk-adjusted return metrics
- Algorithmic trading signals
"""

result = quant_agent.invoke({
    "messages": [{"role": "user", "content": query}]
})
```

## Programmatic Usage Examples

### Example 11: Batch Analysis Script

```python
#!/usr/bin/env python3
"""Batch stock analysis script"""

from research_agent import run_stock_research
import json
import time

# Portfolio of stocks to analyze
portfolio = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
results = {}

for symbol in portfolio:
    print(f"Analyzing {symbol}...")
    
    query = f"""
    Analyze {symbol} and provide:
    1. Current valuation (P/E, P/B, PEG ratios)
    2. Technical momentum (RSI, MACD, trend)
    3. Risk level (1-10 scale)
    4. 12-month price target
    5. Buy/Hold/Sell recommendation
    
    Keep response concise but comprehensive.
    """
    
    try:
        result = run_stock_research(query)
        results[symbol] = {
            "timestamp": time.time(),
            "analysis": result,
            "status": "success"
        }
        print(f"✓ {symbol} analysis completed")
        
    except Exception as e:
        results[symbol] = {
            "timestamp": time.time(),
            "error": str(e),
            "status": "failed"
        }
        print(f"✗ {symbol} analysis failed: {e}")
    
    # Add delay to avoid overwhelming the system
    time.sleep(2)

# Save results
with open("portfolio_analysis.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nBatch analysis completed. Results saved to portfolio_analysis.json")
```

### Example 12: Real-time Monitoring Script

```python
#!/usr/bin/env python3
"""Real-time stock monitoring with alerts"""

import time
import json
from datetime import datetime
from research_agent import get_stock_price

def monitor_stocks(watchlist, alert_thresholds):
    """Monitor stocks and generate alerts based on price movements"""
    
    while True:
        print(f"\n=== Market Check: {datetime.now()} ===")
        
        for symbol, threshold in alert_thresholds.items():
            try:
                # Get current price
                price_data = json.loads(get_stock_price(symbol))
                current_price = price_data.get("current_price")
                
                if current_price:
                    print(f"{symbol}: ${current_price:.2f}")
                    
                    # Check for alerts
                    if current_price >= threshold["high_alert"]:
                        print(f"🚨 HIGH ALERT: {symbol} reached ${current_price:.2f}")
                        # Trigger detailed analysis
                        analysis_query = f"Analyze {symbol} - price hit high alert level of ${threshold['high_alert']}"
                        # Could trigger full analysis here
                        
                    elif current_price <= threshold["low_alert"]:
                        print(f"📉 LOW ALERT: {symbol} dropped to ${current_price:.2f}")
                        # Trigger buying opportunity analysis
                        
            except Exception as e:
                print(f"Error monitoring {symbol}: {e}")
        
        # Wait 5 minutes before next check
        time.sleep(300)

# Configuration
watchlist = ["AAPL", "TSLA", "NVDA", "MSFT"]
alert_thresholds = {
    "AAPL": {"high_alert": 200, "low_alert": 170},
    "TSLA": {"high_alert": 300, "low_alert": 200},
    "NVDA": {"high_alert": 150, "low_alert": 100},
    "MSFT": {"high_alert": 450, "low_alert": 380}
}

if __name__ == "__main__":
    print("Starting stock monitoring...")
    monitor_stocks(watchlist, alert_thresholds)
```

## Integration Examples

### Example 13: Gradio Custom Interface

```python
#!/usr/bin/env python3
"""Custom Gradio interface with advanced features"""

import gradio as gr
from research_agent import run_stock_research
from examples.integration_examples import create_enhanced_research_agent
import json

# Create different agent types
agents = {
    "Standard": None,  # Will use default
    "Enhanced": create_enhanced_research_agent(),
    "ESG Focus": create_specialized_research_agent("esg"),
    "Quantitative": create_specialized_research_agent("quantitative")
}

def analyze_stock(symbol, analysis_type, agent_type, custom_query=""):
    """Enhanced analysis function with multiple options"""
    
    if custom_query:
        query = custom_query
    else:
        # Pre-built query templates
        templates = {
            "Quick Analysis": f"Provide a quick analysis of {symbol} with buy/hold/sell recommendation",
            "Comprehensive": f"Conduct comprehensive analysis of {symbol} including fundamental, technical, and risk analysis",
            "Valuation Focus": f"Focus on valuation analysis of {symbol} - P/E, DCF, comparable companies",
            "Technical Focus": f"Provide detailed technical analysis of {symbol} with entry/exit points",
            "Risk Assessment": f"Conduct thorough risk assessment of {symbol} including all risk categories"
        }
        query = templates.get(analysis_type, templates["Quick Analysis"])
    
    try:
        if agent_type == "Standard":
            result = run_stock_research(query)
        else:
            agent = agents[agent_type]
            response = agent.invoke({"messages": [{"role": "user", "content": query}]})
            result = response["messages"][-1]["content"]
        
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"

# Create interface
with gr.Blocks(title="DeepAgent Stock Research Pro") as demo:
    gr.Markdown("# 📊 DeepAgent Stock Research Professional")
    
    with gr.Row():
        with gr.Column(scale=1):
            symbol_input = gr.Textbox(
                label="Stock Symbol", 
                placeholder="e.g., AAPL, MSFT, TSLA",
                value="AAPL"
            )
            
            analysis_type = gr.Dropdown(
                choices=["Quick Analysis", "Comprehensive", "Valuation Focus", "Technical Focus", "Risk Assessment"],
                label="Analysis Type",
                value="Quick Analysis"
            )
            
            agent_type = gr.Dropdown(
                choices=["Standard", "Enhanced", "ESG Focus", "Quantitative"],
                label="Agent Type",
                value="Standard"
            )
            
            custom_query = gr.Textbox(
                label="Custom Query (Optional)",
                placeholder="Override analysis type with custom query",
                lines=3
            )
            
            analyze_btn = gr.Button("🔍 Analyze", variant="primary")
            
        with gr.Column(scale=2):
            output = gr.Textbox(
                label="Analysis Report",
                lines=25,
                max_lines=50
            )
    
    # Examples section
    gr.Markdown("## Example Queries")
    examples = gr.Examples(
        examples=[
            ["AAPL", "Comprehensive", "Enhanced", ""],
            ["TSLA", "Risk Assessment", "Standard", ""],
            ["MSFT", "Valuation Focus", "Quantitative", ""],
            ["NVDA", "Technical Focus", "Standard", ""],
            ["", "", "ESG Focus", "Compare ESG scores of AAPL, MSFT, and GOOGL"]
        ],
        inputs=[symbol_input, analysis_type, agent_type, custom_query]
    )
    
    analyze_btn.click(
        fn=analyze_stock,
        inputs=[symbol_input, analysis_type, agent_type, custom_query],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
```

### Example 14: API Integration

```python
#!/usr/bin/env python3
"""REST API wrapper for DeepAgent Stock Research"""

from flask import Flask, request, jsonify
from research_agent import run_stock_research
import json
import time

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
def analyze_stock():
    """API endpoint for stock analysis"""
    try:
        data = request.get_json()
        
        symbol = data.get('symbol', '').upper()
        analysis_type = data.get('type', 'standard')
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        
        # Build query based on analysis type
        queries = {
            "standard": f"Analyze {symbol} and provide investment recommendation",
            "detailed": f"Conduct comprehensive analysis of {symbol} including all aspects",
            "technical": f"Provide technical analysis of {symbol} with trading signals",
            "fundamental": f"Focus on fundamental analysis of {symbol} - financials and valuation",
            "risk": f"Conduct risk assessment of {symbol}"
        }
        
        query = queries.get(analysis_type, queries["standard"])
        
        # Add custom parameters if provided
        if data.get('custom_query'):
            query = data['custom_query']
        
        # Perform analysis
        start_time = time.time()
        result = run_stock_research(query)
        analysis_time = time.time() - start_time
        
        return jsonify({
            "success": True,
            "symbol": symbol,
            "analysis_type": analysis_type,
            "analysis": result,
            "analysis_time": round(analysis_time, 2),
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": time.time()
        }), 500

@app.route('/api/batch', methods=['POST'])
def batch_analyze():
    """Batch analysis endpoint"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        analysis_type = data.get('type', 'standard')
        
        if not symbols:
            return jsonify({"error": "Symbols list is required"}), 400
        
        results = {}
        for symbol in symbols:
            try:
                query = f"Quick analysis of {symbol} - price, trend, recommendation"
                result = run_stock_research(query)
                results[symbol] = {"success": True, "analysis": result}
            except Exception as e:
                results[symbol] = {"success": False, "error": str(e)}
        
        return jsonify({
            "success": True,
            "results": results,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": time.time()
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Real-World Scenarios

### Example 15: Portfolio Rebalancing Analysis

**Query:**
```
I have a $500,000 portfolio currently allocated as:
- 40% AAPL ($200,000)
- 30% MSFT ($150,000) 
- 20% GOOGL ($100,000)
- 10% TSLA ($50,000)

Market conditions have changed. Analyze each position and recommend:
1. Which positions to increase/decrease
2. Optimal rebalancing strategy
3. New target allocations
4. Tax implications of rebalancing
5. Risk assessment of current vs proposed portfolio
```

### Example 16: Earnings Season Analysis

**Query:**
```
Apple (AAPL) is announcing earnings next week. Provide:
1. Earnings expectations vs consensus estimates
2. Key metrics and guidance to watch
3. Historical earnings reaction patterns
4. Options strategies for the announcement
5. Post-earnings price targets (bull/bear scenarios)
6. Position sizing recommendations before earnings
```

### Example 17: Market Crash Analysis

**Query:**
```
The market has dropped 15% this week. Analyze the following for investment opportunities:
- Quality stocks: AAPL, MSFT, JNJ, KO
- Growth stocks: NVDA, TSLA, SHOP, ROKU
- Value opportunities: BRK.B, JPM, WMT, XOM

For each category:
1. Which stocks offer the best risk-adjusted opportunities
2. Appropriate entry points and position sizing
3. Expected recovery timeframes
4. Risk management strategies
```

### Example 18: Retirement Portfolio Analysis

**Query:**
```
Analyze this retirement portfolio for a 55-year-old investor:
Current holdings: 60% stocks, 40% bonds
Stock allocation: SPY (30%), AAPL (10%), MSFT (8%), GOOGL (6%), JNJ (6%)

Goals:
- 10-year investment horizon
- Moderate risk tolerance
- $2M target portfolio value
- Monthly income generation

Recommend:
1. Asset allocation adjustments
2. Individual stock vs ETF strategy
3. Dividend-focused additions
4. Risk reduction timeline
5. Rebalancing frequency
```

## Query Optimization Tips

### For Better Results:

1. **Be Specific**: Include timeframes, investment goals, risk tolerance
2. **Multiple Aspects**: Ask for fundamental, technical, and risk analysis
3. **Context**: Provide portfolio context, market conditions, personal situation
4. **Actionable Requests**: Ask for specific recommendations, entry points, position sizing

### Example of Well-Structured Query:
```
I'm a growth-oriented investor with a 5-year horizon and moderate-high risk tolerance. 
Analyze Nvidia (NVDA) for a $50,000 investment:

1. Fundamental Analysis:
   - Revenue growth sustainability
   - AI market opportunity assessment
   - Competitive moat evaluation
   - Valuation vs growth prospects

2. Technical Analysis:
   - Current trend and momentum
   - Key support/resistance levels
   - Optimal entry strategy
   - Stop-loss recommendations

3. Risk Assessment:
   - Regulatory risks in AI/chips
   - Competition from AMD/Intel
   - China market exposure
   - Valuation risks

4. Portfolio Integration:
   - Position sizing for my $500k portfolio
   - Correlation with existing tech holdings
   - Sector concentration risks

Provide specific buy/hold/sell recommendation with price targets and reasoning.
```

This comprehensive approach will generate the most valuable and actionable analysis from the DeepAgent system.