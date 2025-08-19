from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import yfinance as yf
import logging
import gradio as gr
from langchain_core.tools import tool
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# 1. Create an Ollama model
ollama_model = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "gpt-oss"),
    temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0")),
    base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    request_timeout=60
)


@tool
def get_stock_price(symbol: str) -> str:
    """Get current stock price and basic information."""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period="1d")
        if hist.empty:
            logging.error("No historical data found")
            return json.dumps({"error": f"Could not retrieve data for {symbol}"})
            
        current_price = hist['Close'].iloc[-1]
        result = {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "company_name": info.get('longName', symbol),
            "market_cap": info.get('marketCap', 0),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "52_week_high": info.get('fiftyTwoWeekHigh', 0),
            "52_week_low": info.get('fiftyTwoWeekLow', 0)
        }
        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def get_financial_statements(symbol: str) -> str:
    """Retrieve key financial statement data."""
    try:
        stock = yf.Ticker(symbol)
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        
        latest_year = financials.columns[0]
        
        return json.dumps({
            "symbol": symbol,
            "period": str(latest_year.year),
            "revenue": float(financials.loc['Total Revenue', latest_year]) if 'Total Revenue' in financials.index else 'N/A',
            "net_income": float(financials.loc['Net Income', latest_year]) if 'Net Income' in financials.index else 'N/A',
            "total_assets": float(balance_sheet.loc['Total Assets', latest_year]) if 'Total Assets' in balance_sheet.index else 'N/A',
            "total_debt": float(balance_sheet.loc['Total Debt', latest_year]) if 'Total Debt' in balance_sheet.index else 'N/A'
        }, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_technical_indicators(symbol: str, period: str = "3mo") -> str:
    """Calculate key technical indicators."""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        
        if hist.empty:
            return f"Error: No historical data for {symbol}"
        
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        latest = hist.iloc[-1]
        latest_rsi = rsi.iloc[-1]
        
        return json.dumps({
            "symbol": symbol,
            "current_price": round(latest['Close'], 2),
            "sma_20": round(latest['SMA_20'], 2),
            "sma_50": round(latest['SMA_50'], 2),
            "rsi": round(latest_rsi, 2),
            "volume": int(latest['Volume']),
            "trend_signal": "bullish" if latest['Close'] > latest['SMA_20'] > latest['SMA_50'] else "bearish"
        }, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


# Create prompt template for the agent
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an elite stock research analyst with access to financial data tools. 

Your research process should be systematic and comprehensive:

1. **Initial Data Gathering**: Start by collecting basic stock information, price data, and recent financial data
2. **Fundamental Analysis**: Deep dive into financial statements, ratios, and company fundamentals
3. **Technical Analysis**: Analyze price patterns, trends, and technical indicators
4. **Risk Assessment**: Identify and evaluate potential risks
5. **Competitive Analysis**: Compare with industry peers when relevant
6. **Synthesis**: Combine all findings into a coherent investment thesis
7. **Recommendation**: Provide clear buy/sell/hold recommendation with price targets

Always:
- Use specific data and numbers to support your analysis
- Cite your sources and methodology
- Consider multiple perspectives and potential scenarios
- Provide actionable insights and concrete recommendations
- Structure your final report professionally"""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Define all tools
tools = [
    get_stock_price,
    get_financial_statements, 
    get_technical_indicators
]

# Create the LangChain agent
agent = create_tool_calling_agent(ollama_model, tools, prompt_template)
stock_research_agent = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)





def run_stock_research(query: str):
    """Run the stock research agent and return the analysis."""
    try:
        result = stock_research_agent.invoke({"input": query})
        output_text = result.get("output", "")
        
        if not output_text:
            output_text = "Error: No response received from agent."
        
        return output_text

    except Exception as e:
        return f"Error: {str(e)}\n\nPlease ensure Ollama is running and the model is available."

# Launch app
if __name__ == "__main__":
    # Create Gradio UI
    with gr.Blocks() as demo:
        gr.Markdown("## 📊 Stock Research Agent")
        gr.Markdown("Enter your stock research request below. Example: *Comprehensive analysis on Apple Inc. (AAPL)*")
        
        with gr.Row():
            query_input = gr.Textbox(label="Research Query", lines=6, placeholder="Type your research query here...")
        
        run_button = gr.Button("Run Analysis")
        output_box = gr.Textbox(label="Research Report", lines=20)
        
        run_button.click(fn=run_stock_research, inputs=query_input, outputs=output_box)
    
    port = int(os.getenv("GRADIO_PORT", "7860"))
    host = os.getenv("GRADIO_HOST", "127.0.0.1")
    share = os.getenv("GRADIO_SHARE", "false").lower() == "true"
    
    print(f"🚀 Starting DeepAgent Stock Research...")
    print(f"📊 Web interface: http://{host}:{port}")
    print(f"🤖 Model: {ollama_model.model}")
    
    demo.launch(server_name=host, server_port=port, share=share)
