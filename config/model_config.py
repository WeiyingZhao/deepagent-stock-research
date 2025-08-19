"""
Model Configuration Examples
This file shows how to customize the LLM model configuration
"""

from langchain_ollama import ChatOllama
import os

# Default configuration (used in main application)
DEFAULT_MODEL_CONFIG = {
    "model": "gpt-oss",
    "temperature": 0,
}

# Alternative model configurations
ALTERNATIVE_MODELS = {
    "creative": {
        "model": "llama2",
        "temperature": 0.7,
        "top_p": 0.9,
    },
    "analytical": {
        "model": "codellama", 
        "temperature": 0.1,
        "top_p": 0.8,
    },
    "balanced": {
        "model": "mistral",
        "temperature": 0.3,
        "top_p": 0.85,
    }
}

def create_ollama_model(config_name="default"):
    """Create an Ollama model with specified configuration."""
    if config_name == "default":
        config = DEFAULT_MODEL_CONFIG
    else:
        config = ALTERNATIVE_MODELS.get(config_name, DEFAULT_MODEL_CONFIG)
    
    return ChatOllama(**config)

# Example usage:
# model = create_ollama_model("creative")
# model = create_ollama_model("analytical")