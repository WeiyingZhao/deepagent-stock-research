"""
Integration Examples
Shows how to integrate custom tools with the main application
"""

import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from model_config import create_ollama_model
from custom_tools import CUSTOM_TOOLS, get_tools_by_category

# Import original tools from main application
from research_agent import get_stock_price, get_financial_statements, get_technical_indicators

def create_enhanced_research_agent():
    """Create an enhanced research agent with custom tools."""
    
    # Use alternative model configuration
    model = create_ollama_model("analytical")
    
    # Combine original tools with custom tools
    all_tools = [
        get_stock_price,
        get_financial_statements,
        get_technical_indicators
    ] + CUSTOM_TOOLS
    
    # Enhanced research prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an elite stock research analyst with access to comprehensive analytical tools.
        
        Your enhanced research process:
        1. **Comprehensive Data Gathering**: Use all available tools for market data, financials, news, and insider activity
        2. **Multi-Dimensional Analysis**: Employ fundamental, technical, and sentiment analysis
        3. **Advanced Valuation**: Include DCF models, peer comparisons, and intrinsic value calculations
        4. **Holistic Risk Assessment**: Consider market, company, and sector-specific risks
        5. **Options and Derivatives**: Analyze options flow and derivative strategies when relevant
        6. **News and Sentiment**: Incorporate recent news, insider trading, and market sentiment
        7. **Actionable Recommendations**: Provide specific entry/exit points, position sizing, and risk management
        
        Available tools: {tools}
        
        Use this format:
        Thought: I need to gather comprehensive data for this analysis
        Action: [tool name]
        Action Input: [input to tool]
        Observation: [result]
        ... (repeat as needed)
        Thought: I now have enough information for a comprehensive analysis
        Final Answer: [detailed analysis and recommendations]"""),
        ("user", "{input}"),
        ("assistant", "{agent_scratchpad}")
    ])
    
    agent = create_tool_calling_agent(model, all_tools, prompt)
    return AgentExecutor(agent=agent, tools=all_tools, verbose=True, max_iterations=15)

def create_specialized_research_agent(focus="quantitative"):
    """Create a specialized research agent focused on specific analysis type."""
    
    model = create_ollama_model("default")
    
    # Base tools
    base_tools = [get_stock_price, get_financial_statements, get_technical_indicators]
    
    # Specialized configurations
    if focus == "quantitative":
        tools = base_tools + get_tools_by_category("technical")
        subagents = [get_subagents_by_category("quantitative")[0]]
        instructions = """You are a quantitative research specialist focused on mathematical 
        models, statistical analysis, and algorithmic approaches to stock analysis."""
        
    elif focus == "esg":
        tools = base_tools + get_tools_by_category("sentiment")
        subagents = [get_subagents_by_category("sustainability")[0]]
        instructions = """You are an ESG research specialist focused on sustainable investing 
        and ESG factor analysis for investment decisions."""
        
    elif focus == "options":
        tools = base_tools + [get_tools_by_category("technical")[0]]  # options flow tool
        subagents = [get_subagents_by_category("derivatives")[0]]
        instructions = """You are an options specialist focused on derivatives analysis, 
        volatility trading, and options strategies."""
        
    else:
        # Default to comprehensive analysis
        tools = base_tools + CUSTOM_TOOLS
        subagents = CUSTOM_SUBAGENTS[:3]  # First 3 custom sub-agents
        instructions = """You are a comprehensive research analyst with access to 
        multiple specialized tools and analysis capabilities."""
    
    return create_deep_agent(
        tools=tools,
        instructions=instructions,
        subagents=subagents,
        model=model
    )

def run_enhanced_analysis(query: str, agent_type="enhanced"):
    """Run analysis with enhanced or specialized agent."""
    
    if agent_type == "enhanced":
        agent = create_enhanced_research_agent()
    else:
        agent = create_specialized_research_agent(agent_type)
    
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        messages = result.get("messages", [])
        if messages:
            if isinstance(messages[-1], dict):
                return messages[-1].get("content", "No content available")
            elif hasattr(messages[-1], "content"):
                return messages[-1].content
            else:
                return "Invalid message format"
        else:
            return "No response received"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Example 1: Enhanced comprehensive analysis
    query1 = "Analyze Tesla (TSLA) with comprehensive ESG and sector analysis"
    result1 = run_enhanced_analysis(query1, "enhanced")
    print("=== Enhanced Analysis ===")
    print(result1[:500] + "..." if len(result1) > 500 else result1)
    
    # Example 2: ESG-focused analysis
    query2 = "Evaluate Microsoft (MSFT) from an ESG perspective"
    result2 = run_enhanced_analysis(query2, "esg")
    print("\n=== ESG-Focused Analysis ===")
    print(result2[:500] + "..." if len(result2) > 500 else result2)
    
    # Example 3: Options-focused analysis
    query3 = "Analyze NVIDIA (NVDA) options flow and recommend strategies"
    result3 = run_enhanced_analysis(query3, "options")
    print("\n=== Options-Focused Analysis ===")
    print(result3[:500] + "..." if len(result3) > 500 else result3)