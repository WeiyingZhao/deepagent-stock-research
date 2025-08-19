# Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: 2GB free space for dependencies and models
- **Internet**: Required for real-time financial data

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/deepagent-stock-research.git
cd deepagent-stock-research
```

### 2. Create Virtual Environment (Recommended)

```bash
# Using venv
python -m venv deepagent-env
source deepagent-env/bin/activate  # On Windows: deepagent-env\Scripts\activate

# Using conda
conda create -n deepagent-env python=3.9
conda activate deepagent-env
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure Ollama

#### Option A: Automatic Installation (Linux/macOS)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Option B: Manual Installation
1. Download from [Ollama website](https://ollama.ai)
2. Follow platform-specific installation instructions

#### Download Required Model
```bash
ollama pull gpt-oss
```

### 5. Verify Installation

```bash
python -c "import deepagents, yfinance, gradio; print('All dependencies installed successfully')"
```

### 6. Run the Application

```bash
python research_agent.py
```

The application will start on `http://localhost:7860`

## Alternative Model Setup

### Using Different Models

```bash
# For more creative analysis
ollama pull llama2

# For code-focused analysis  
ollama pull codellama

# For general purpose
ollama pull mistral
```

Update the model in `research_agent.py`:
```python
ollama_model = ChatOllama(
    model="llama2",  # Change to your preferred model
    temperature=0,
)
```

## Docker Installation (Alternative)

### Using Docker

1. **Build the container:**
```bash
docker build -t deepagent-stock-research .
```

2. **Run the container:**
```bash
docker run -p 7860:7860 deepagent-stock-research
```

### Docker Compose
```yaml
version: '3.8'
services:
  deepagent:
    build: .
    ports:
      - "7860:7860"
    environment:
      - OLLAMA_HOST=ollama:11434
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
```

## Configuration Options

### Environment Variables

Create a `.env` file:
```env
# Model Configuration
OLLAMA_MODEL=gpt-oss
OLLAMA_TEMPERATURE=0
OLLAMA_HOST=http://localhost:11434

# Application Settings
GRADIO_PORT=7860
GRADIO_HOST=0.0.0.0
DEBUG_MODE=False

# Data Sources
YAHOO_FINANCE_ENABLED=True
```

### Custom Configuration

1. **Copy example config:**
```bash
cp config/model_config.py.example config/model_config.py
```

2. **Edit configuration:**
```python
# config/model_config.py
DEFAULT_MODEL_CONFIG = {
    "model": "your-model",
    "temperature": 0.1,
    # Add other parameters
}
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```bash
   # Check if Ollama is running
   ollama list
   
   # Restart Ollama service
   sudo systemctl restart ollama  # Linux
   brew services restart ollama   # macOS
   ```

2. **Port Already in Use**
   ```bash
   # Change port in research_agent.py
   demo.launch(server_port=7861)
   ```

3. **Memory Issues**
   ```bash
   # Use smaller model
   ollama pull phi
   ```

4. **Dependencies Conflicts**
   ```bash
   # Clean install
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

### Getting Help

- Check the [troubleshooting guide](troubleshooting.md)
- Review [common issues](https://github.com/yourusername/deepagent-stock-research/issues)
- Join our [Discord community](https://discord.gg/deepagents)

## Next Steps

1. Read the [User Guide](user_guide.md)
2. Explore [Example Queries](../examples/sample_queries.md)
3. Try [Custom Configurations](api_reference.md)
4. Check [Best Practices](best_practices.md)