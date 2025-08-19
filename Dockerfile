# DeepAgent Stock Research - Docker Image

FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs config examples screenshots

# Create non-root user for security
RUN groupadd -r deepagent && \
    useradd -r -g deepagent deepagent && \
    chown -R deepagent:deepagent /app

# Switch to non-root user
USER deepagent

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Expose port
EXPOSE 7860

# Default environment variables
ENV GRADIO_HOST=0.0.0.0 \
    GRADIO_PORT=7860 \
    OLLAMA_HOST=http://ollama:11434 \
    LOG_LEVEL=INFO

# Run the application
CMD ["python", "research_agent.py"]