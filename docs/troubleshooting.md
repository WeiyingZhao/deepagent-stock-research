# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### 1. Dependency Installation Failures

**Problem:** `pip install -r requirements.txt` fails with package conflicts.

**Solutions:**
```bash
# Create clean virtual environment
python -m venv fresh-env
source fresh-env/bin/activate  # Windows: fresh-env\Scripts\activate

# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Install dependencies one by one to identify conflicts
pip install deepagents
pip install langchain-ollama
pip install langchain-core
pip install yfinance
pip install gradio
pip install pandas
pip install numpy

# Alternative: Use conda for package management
conda create -n deepagent python=3.9
conda activate deepagent
pip install -r requirements.txt
```

#### 2. Python Version Compatibility

**Problem:** Application fails with Python version errors.

**Solutions:**
```bash
# Check Python version
python --version

# Ensure Python 3.8+
# If using older version, install newer Python
# macOS
brew install python@3.9

# Ubuntu/Debian
sudo apt update
sudo apt install python3.9

# Windows: Download from python.org
```

### Ollama Issues

#### 1. Ollama Installation Problems

**Problem:** Ollama installation script fails or service won't start.

**Solutions:**

**Linux/macOS:**
```bash
# Manual installation
# Download appropriate binary from https://ollama.ai
chmod +x ollama-linux  # or ollama-darwin
sudo mv ollama-linux /usr/local/bin/ollama

# Start service
ollama serve

# In another terminal
ollama pull gpt-oss
```

**Windows:**
```powershell
# Download Windows installer from ollama.ai
# Run as administrator
# Or use WSL2 for Linux installation
```

#### 2. Model Download Issues

**Problem:** `ollama pull gpt-oss` fails or hangs.

**Solutions:**
```bash
# Check available models
ollama list

# Try alternative models
ollama pull llama2
ollama pull phi
ollama pull mistral

# If network issues, use smaller model first
ollama pull phi  # Smaller model

# Update model in research_agent.py
# Line 16: model="phi"
```

#### 3. Ollama Connection Errors

**Problem:** Application can't connect to Ollama service.

**Solutions:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama service
ollama serve

# Check port availability
netstat -an | grep 11434

# If port conflict, change port
OLLAMA_PORT=11435 ollama serve

# Update connection in code
# ChatOllama(base_url="http://localhost:11435")
```

### Application Runtime Issues

#### 1. Gradio Interface Won't Load

**Problem:** Browser shows "Connection refused" or timeout.

**Solutions:**
```bash
# Check if port 7860 is available
netstat -an | grep 7860

# Use different port
# In research_agent.py, line 245:
demo.launch(server_port=7861)

# Check firewall settings
# Allow incoming connections on port 7860

# For remote access
demo.launch(server_name="0.0.0.0", server_port=7860)
```

#### 2. Stock Data Retrieval Errors

**Problem:** Yahoo Finance data fetching fails.

**Solutions:**
```python
# Test yfinance directly
import yfinance as yf
ticker = yf.Ticker("AAPL")
print(ticker.info)  # Should return data

# If fails, check network connectivity
# Some corporate networks block yfinance

# Alternative: Use different data source
# Implement Alpha Vantage or other API
```

#### 3. Memory Issues

**Problem:** Application crashes with memory errors.

**Solutions:**
```bash
# Monitor memory usage
top -p $(pgrep -f research_agent.py)

# Use lighter model
ollama pull phi  # Much smaller than gpt-oss

# Reduce context window
# In research_agent.py:
ollama_model = ChatOllama(
    model="phi",
    temperature=0,
    max_tokens=1024  # Reduce from default
)

# Add memory limits to Docker if using containers
docker run -m 4g deepagent-stock-research
```

### Performance Issues

#### 1. Slow Response Times

**Problem:** Analysis takes very long to complete.

**Solutions:**
```python
# Use faster model
ollama_model = ChatOllama(
    model="phi",  # Faster than gpt-oss
    temperature=0
)

# Reduce number of sub-agents
subagents = [fundamental_analyst]  # Use only one

# Simplify instructions
research_instructions = """Provide concise stock analysis focusing on:
1. Current price and basic metrics
2. Simple buy/hold/sell recommendation
Keep response under 500 words."""

# Enable request timeouts
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Add timeout handling in tools
```

#### 2. High CPU Usage

**Problem:** System becomes unresponsive during analysis.

**Solutions:**
```bash
# Limit CPU cores for Ollama
OLLAMA_NUM_CORES=2 ollama serve

# Use process priority
nice -n 10 python research_agent.py

# Monitor and limit processes
ulimit -u 50  # Limit user processes
```

### Development Issues

#### 1. Import Errors

**Problem:** Module import failures in custom configurations.

**Solutions:**
```python
# Fix Python path issues
import sys
import os
sys.path.append(os.path.dirname(__file__))

# Use absolute imports
from research_agent import get_stock_price

# Check file structure
ls -la config/
ls -la examples/
```

#### 2. Configuration File Issues

**Problem:** Custom configurations not loading properly.

**Solutions:**
```python
# Verify file existence
import os
config_path = "config/model_config.py"
print(f"Config exists: {os.path.exists(config_path)}")

# Check syntax
python -m py_compile config/model_config.py

# Debug imports
try:
    from config.model_config import create_ollama_model
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
```

### Data Issues

#### 1. Invalid Stock Symbols

**Problem:** Analysis fails for certain stock symbols.

**Solutions:**
```python
# Add symbol validation
import yfinance as yf

def validate_symbol(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return 'longName' in info or 'shortName' in info
    except:
        return False

# Test before analysis
if not validate_symbol("INVALID"):
    return "Invalid stock symbol"
```

#### 2. Market Hours Issues

**Problem:** Real-time data unavailable outside market hours.

**Solutions:**
```python
# Check market status
from datetime import datetime, time
import pytz

def is_market_open():
    ny_tz = pytz.timezone('America/New_York')
    now = datetime.now(ny_tz)
    market_open = time(9, 30)
    market_close = time(16, 0)
    
    return (now.weekday() < 5 and 
            market_open <= now.time() <= market_close)

# Adjust messaging for closed markets
if not is_market_open():
    return "Note: Markets are currently closed. Showing last available data."
```

## Debugging Tips

### Enable Debug Logging

```python
import logging

# In research_agent.py, add more detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# Add debug prints in functions
logger = logging.getLogger(__name__)
logger.debug(f"Processing symbol: {symbol}")
```

### Test Individual Components

```python
# Test model connection
try:
    model = ChatOllama(model="gpt-oss", temperature=0)
    response = model.invoke("Hello")
    print("Model working:", response)
except Exception as e:
    print("Model error:", e)

# Test tools individually
result = get_stock_price("AAPL")
print("Tool result:", result)

# Test data sources
import yfinance as yf
ticker = yf.Ticker("AAPL")
print("Yahoo Finance:", ticker.history(period="1d"))
```

### Check System Resources

```bash
# Memory usage
free -h

# Disk space
df -h

# CPU usage
htop

# Network connectivity
ping -c 4 finance.yahoo.com
```

## Getting Help

### Support Channels

1. **GitHub Issues**: Report bugs and feature requests
2. **Discord Community**: Real-time help and discussions
3. **Documentation**: Check docs/ directory for guides
4. **Stack Overflow**: Tag questions with `deepagents`

### When Reporting Issues

Include the following information:

1. **Environment:**
   - Python version
   - Operating system
   - Ollama version
   - Dependencies versions

2. **Error Details:**
   - Full error traceback
   - Steps to reproduce
   - Expected vs actual behavior

3. **System Information:**
   ```bash
   # Generate system info
   python -c "
   import sys, platform
   print(f'Python: {sys.version}')
   print(f'Platform: {platform.platform()}')
   print(f'Architecture: {platform.architecture()}')
   "
   
   ollama --version
   pip freeze > requirements-actual.txt
   ```

### Quick Diagnostics Script

```python
#!/usr/bin/env python3
"""Quick diagnostics for DeepAgent Stock Research"""

import sys
import subprocess
import importlib

def check_python():
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    return version >= (3, 8)

def check_dependencies():
    deps = ['deepagents', 'langchain_ollama', 'yfinance', 'gradio', 'pandas', 'numpy']
    results = {}
    
    for dep in deps:
        try:
            module = importlib.import_module(dep)
            results[dep] = getattr(module, '__version__', 'unknown')
        except ImportError:
            results[dep] = 'NOT INSTALLED'
    
    return results

def check_ollama():
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    print("=== DeepAgent Diagnostics ===")
    
    print("\n1. Python Check:")
    python_ok = check_python()
    print(f"   Status: {'✓' if python_ok else '✗'}")
    
    print("\n2. Dependencies:")
    deps = check_dependencies()
    for dep, version in deps.items():
        status = '✓' if version != 'NOT INSTALLED' else '✗'
        print(f"   {dep}: {status} {version}")
    
    print("\n3. Ollama Check:")
    ollama_ok = check_ollama()
    print(f"   Status: {'✓' if ollama_ok else '✗'}")
    
    print(f"\n=== Summary ===")
    overall = python_ok and ollama_ok and all(v != 'NOT INSTALLED' for v in deps.values())
    print(f"Overall Status: {'✓ READY' if overall else '✗ ISSUES FOUND'}")
```

Run this script to quickly identify configuration issues:
```bash
python diagnostics.py
```