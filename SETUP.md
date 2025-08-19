# Complete Setup Guide

## Prerequisites Check

Before starting, verify your system meets these requirements:

```bash
# Check Python version (must be 3.8+)
python --version
# Should show: Python 3.8.x or higher

# Check if pip is available
pip --version

# Check available memory (recommended 8GB+)
# On macOS/Linux:
free -h
# On macOS:
vm_stat | head -5
```

## Step 1: Environment Setup

### Option A: Using Virtual Environment (Recommended)

```bash
# Navigate to your desired directory
cd ~/projects  # or wherever you want the project

# Clone or download the project
git clone https://github.com/yourusername/deepagent-stock-research.git
cd deepagent-stock-research

# Create virtual environment
python -m venv deepagent-env

# Activate virtual environment
# On macOS/Linux:
source deepagent-env/bin/activate
# On Windows:
deepagent-env\Scripts\activate

# Verify activation (should show path to virtual env)
which python
```

### Option B: Using Conda

```bash
# Create conda environment
conda create -n deepagent python=3.9 -y
conda activate deepagent

# Navigate to project directory
cd deepagent-stock-research
```

## Step 2: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import langchain, yfinance, gradio; print('✓ All packages installed successfully')"
```

If you encounter issues, install packages individually:

```bash
pip install langchain
pip install langchain-ollama
pip install langchain-core
pip install langchain-community
pip install yfinance
pip install gradio
pip install pandas
pip install numpy
pip install requests
pip install python-dotenv
```

**Note:** The corrected requirements.txt now contains:
- `langchain` (core framework)
- `langchain-ollama` (Ollama integration)
- `langchain-core` (core components)
- `langchain-community` (community tools)
- `yfinance` (financial data)
- `gradio` (web interface)
- `pandas` & `numpy` (data processing)
- `requests` (HTTP requests)
- `python-dotenv` (environment variables)

## Step 3: Ollama Installation and Setup

### Install Ollama

#### macOS/Linux (Automatic):
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS (Using Homebrew):
```bash
brew install ollama
```

#### Windows:
1. Download installer from [ollama.ai](https://ollama.ai)
2. Run the installer as administrator
3. Restart your terminal

#### Verify Installation:
```bash
ollama --version
# Should show version information
```

### Start Ollama Service

```bash
# Start Ollama (keep this terminal open)
ollama serve

# In a new terminal window, test connection
ollama list
# Should show available models (may be empty initially)
```

### Download Required Models

```bash
# Download the default model (this may take 5-15 minutes)
ollama pull gpt-oss

# Optional: Download alternative models
ollama pull llama2    # For more creative analysis
ollama pull phi       # Lightweight, faster model
ollama pull mistral   # Balanced performance

# Verify models are downloaded
ollama list
```

## Step 4: Test Basic Setup

```bash
# Test Python environment
python -c "
import langchain
from langchain_ollama import ChatOllama
import yfinance as yf
import gradio as gr
import pandas as pd
from langchain_core.tools import tool
print('✓ All Python packages working')
print('✓ LangChain version:', langchain.__version__)

# Test Yahoo Finance connection
ticker = yf.Ticker('AAPL')
data = ticker.history(period='1d')
print(f'✓ Yahoo Finance working - AAPL price: ${data[\"Close\"].iloc[-1]:.2f}')
"
```

```bash
# Test Ollama connection
python -c "
from langchain_ollama import ChatOllama
try:
    model = ChatOllama(model='gpt-oss', temperature=0)
    response = model.invoke('Hello')
    print('✓ Ollama connection working')
    print('✓ Model response received')
except Exception as e:
    print(f'✗ Ollama error: {e}')
    print('Make sure ollama serve is running and gpt-oss model is downloaded')
"
```

```bash
# Test the corrected research agent
python -c "
from research_agent import get_stock_price, ollama_model
import json

# Test stock price tool
result = get_stock_price('AAPL')
data = json.loads(result)
print('✓ Stock price tool working')
print(f'✓ AAPL current price: ${data[\"current_price\"]}')

# Test model configuration
print('✓ Model configured:', ollama_model.model)
print('✓ Base URL:', ollama_model.base_url)
"
```

## Step 5: Run the Application

```bash
# Start the main application
python research_agent.py
```

You should see output like:
```
🚀 Starting DeepAgent Stock Research...
📊 Web interface will be available at: http://127.0.0.1:7860
🔧 Using Ollama model: gpt-oss
🌐 Ollama host: http://localhost:11434
⚙️  Debug mode: True
Running on local URL:  http://127.0.0.1:7860

To create a public link, set `share=True` in `launch()`.
```

Open your browser and navigate to `http://localhost:7860`

**Alternative startup methods:**
```bash
# Using the startup script
./start_deepagent.sh

# Using environment variables
GRADIO_PORT=8080 python research_agent.py

# Using custom model
OLLAMA_MODEL=llama2 python research_agent.py
```

## Step 6: First Test Query

In the web interface, try this simple query:
```
Analyze Apple Inc. (AAPL) and provide a brief investment recommendation.
```

Expected response should include:
- Current stock price
- Basic financial metrics
- Technical indicators
- Investment recommendation (BUY/HOLD/SELL)

## Advanced Configuration

### Environment Variables Setup

Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << 'EOF'
# Model Configuration
OLLAMA_MODEL=gpt-oss
OLLAMA_TEMPERATURE=0
OLLAMA_HOST=http://localhost:11434

# Application Settings
GRADIO_PORT=7860
GRADIO_HOST=127.0.0.1
DEBUG_MODE=true

# Data Sources
YAHOO_FINANCE_ENABLED=true
CACHE_DURATION=300

# Logging
LOG_LEVEL=INFO
LOG_FILE=deepagent.log
EOF
```

### Custom Model Configuration

```bash
# Test different models
python -c "
from config.model_config import create_ollama_model

# Test analytical model (lower temperature)
model = create_ollama_model('analytical')
print('✓ Analytical model ready')

# Test creative model (higher temperature) 
model = create_ollama_model('creative')
print('✓ Creative model ready')
"
```

## Troubleshooting Common Issues

### Issue 1: Package Installation Errors
```bash
# If using wrong Python environment
which python
which pip

# Use Python's pip directly
python -m pip install -r requirements.txt

# For conda environments
conda activate your-env
pip install -r requirements.txt
```

### Issue 2: Import Errors
```bash
# Test imports one by one
python -c "import langchain; print('LangChain OK')"
python -c "from langchain_ollama import ChatOllama; print('Ollama OK')"
python -c "import yfinance; print('YFinance OK')"

# If langchain import fails
pip install --upgrade langchain langchain-core langchain-community
```

### Issue 3: Ollama Connection Failed
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it
ollama serve

# Check port availability
netstat -an | grep 11434
# Should show LISTEN status

# Test Ollama directly
ollama list
curl http://localhost:11434/api/version
```

### Issue 4: Model Download Failed
```bash
# Try smaller model first
ollama pull phi

# Update .env file:
# OLLAMA_MODEL=phi

# Or check network connectivity
ping ollama.ai
```

### Issue 5: Port 7860 Already in Use
```bash
# Find what's using the port
lsof -i :7860

# Use different port via environment variable
GRADIO_PORT=7861 python research_agent.py

# Or edit .env file:
# GRADIO_PORT=7861
```

### Issue 6: Yahoo Finance Data Error
```bash
# Test direct connection
python -c "
import yfinance as yf
ticker = yf.Ticker('AAPL')
data = ticker.history(period='1d')
print('Data received:', not data.empty)
"

# If this fails, check network or try VPN
```

### Issue 7: Agent Creation Errors
```bash
# Test the corrected agent components
python -c "
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_ollama import ChatOllama
from research_agent import tools, prompt_template
print('✓ Agent components working')
"
```

## Performance Optimization

### For Low-Memory Systems
```bash
# Use lightweight model
ollama pull phi

# Update .env file:
# OLLAMA_MODEL=phi
# MAX_TOKENS=1024

# Or set environment variables:
OLLAMA_MODEL=phi python research_agent.py
```

### For Faster Response
```bash
# Use faster model
ollama pull phi

# Reduce agent iterations in .env:
# MAX_ITERATIONS=5

# Enable caching in .env:
# ENABLE_CACHING=true
# CACHE_DURATION=600
```

## Verification Script

Create and run this verification script:

```bash
cat > verify_setup.py << 'EOF'
#!/usr/bin/env python3
"""Setup verification script"""

import sys
import subprocess
import importlib
from datetime import datetime

def check_python():
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    return version >= (3, 8)

def check_packages():
    packages = {
        'langchain': 'langchain',
        'langchain_ollama': 'langchain-ollama', 
        'langchain_core': 'langchain-core',
        'langchain_community': 'langchain-community',
        'yfinance': 'yfinance',
        'gradio': 'gradio',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'requests': 'requests',
        'python-dotenv': 'dotenv'
    }
    
    results = {}
    for pkg_name, import_name in packages.items():
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'unknown')
            results[pkg_name] = f"✓ {version}"
        except ImportError:
            results[pkg_name] = "✗ NOT INSTALLED"
    
    return results

def check_ollama():
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def check_yfinance():
    try:
        import yfinance as yf
        ticker = yf.Ticker('AAPL')
        data = ticker.history(period='1d')
        return not data.empty
    except:
        return False

def check_ollama_model():
    try:
        from langchain_ollama import ChatOllama
        model = ChatOllama(model='gpt-oss', temperature=0)
        response = model.invoke('test')
        return True
    except:
        return False

def check_research_agent():
    try:
        from research_agent import get_stock_price, ollama_model, stock_research_agent
        # Test stock price tool
        result = get_stock_price('AAPL')
        return 'current_price' in result
    except:
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("DeepAgent Stock Research - Setup Verification")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    
    # Check Python
    print(f"\n1. Python: {'✓' if check_python() else '✗'}")
    
    # Check packages
    print("\n2. Python Packages:")
    packages = check_packages()
    for pkg, status in packages.items():
        print(f"   {pkg}: {status}")
    
    # Check Ollama
    print(f"\n3. Ollama Service: {'✓' if check_ollama() else '✗'}")
    
    # Check Yahoo Finance
    print(f"\n4. Yahoo Finance: {'✓' if check_yfinance() else '✗'}")
    
    # Check Ollama Model
    print(f"\n5. Ollama Model: {'✓' if check_ollama_model() else '✗'}")
    
    # Check Research Agent
    print(f"\n6. Research Agent: {'✓' if check_research_agent() else '✗'}")
    
    # Overall status
    all_checks = [
        check_python(),
        all('✓' in status for status in packages.values()),
        check_ollama(),
        check_yfinance(),
        check_ollama_model(),
        check_research_agent()
    ]
    
    print("\n" + "=" * 50)
    overall = all(all_checks)
    print(f"Overall Status: {'✓ READY TO USE' if overall else '✗ SETUP INCOMPLETE'}")
    
    if not overall:
        print("\nPlease review the failed checks above and follow the setup guide.")
    else:
        print("\nYou can now run: python research_agent.py")
    print("=" * 50)
EOF

python verify_setup.py
```

## Next Steps

After successful setup:

1. **Read the Documentation**:
   - `docs/api_reference.md` - Understand available tools and components
   - `examples/sample_queries.md` - Try different analysis types
   - `USAGE_EXAMPLES.md` - Comprehensive usage examples

2. **Explore Examples**:
   ```bash
   # Try the integration examples (if Ollama is running)
   python examples/integration_examples.py
   ```

3. **Customize Configuration**:
   - Edit `.env` file for model and application settings
   - Modify `config/model_config.py` for different model behaviors
   - Add custom tools in `config/custom_tools.py`

4. **Test Different Queries**:
   ```
   # Simple analysis
   Analyze Apple Inc. (AAPL)
   
   # Comprehensive analysis
   Provide detailed analysis of Tesla (TSLA) including fundamental, technical, and risk assessment
   
   # Comparison analysis
   Compare Apple (AAPL) and Microsoft (MSFT) for investment
   ```

5. **Production Deployment**:
   - Review `docs/best_practices.md`
   - Use Docker setup with `docker-compose.yml`
   - Configure environment variables for production
   - Set up monitoring and logging

## Getting Help

If you encounter issues:

1. Check `docs/troubleshooting.md`
2. Run the verification script above
3. Check the GitHub issues page
4. Join our Discord community for real-time support

## Quick Commands Reference

```bash
# Start application
python research_agent.py

# Start with custom settings
OLLAMA_MODEL=gpt-oss GRADIO_PORT=8080 python research_agent.py

# Start Ollama service
ollama serve

# Download models
ollama pull gpt-oss
ollama pull phi          # Lightweight alternative
ollama pull llama2

# Run verification
python verify_setup.py

# Use startup script
./start_deepagent.sh

# Quick installation
./quick_start.sh

# View logs (if enabled)
tail -f deepagent.log

# Check system resources
htop  # or top on macOS

# Test specific components
python -c "from research_agent import get_stock_price; print(get_stock_price('AAPL'))"
```

## Environment Variables Quick Reference

Create or edit `.env` file:
```bash
# Core settings
OLLAMA_MODEL=gpt-oss              # or phi, llama2, mistral
OLLAMA_TEMPERATURE=0              # 0-1, creativity level
GRADIO_PORT=7860                  # Web interface port
GRADIO_HOST=127.0.0.1            # Host interface
DEBUG_MODE=true                   # Enable debug logging

# Performance settings
MAX_ITERATIONS=10                 # Agent iteration limit
ENABLE_CACHING=true              # Enable response caching
CACHE_DURATION=300               # Cache duration in seconds
```