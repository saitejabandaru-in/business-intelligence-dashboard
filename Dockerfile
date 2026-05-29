# Use a secure, slim, official Python runtime as base image
FROM python:3.11-slim

# Set environment variables to optimize Python execution in containers
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory inside the container
WORKDIR /app

# Copy the build configuration and packaging files
COPY pyproject.toml README.md ./
COPY bi_dashboard/ bi_dashboard/

# Install the package locally in the system python environment
RUN pip install --upgrade pip && \
    pip install .

# Expose Streamlit's default port
EXPOSE 8501

# Add a Python-based healthcheck to verify the server is running and healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Launch the Streamlit dashboard via our custom packaged CLI entrypoint
ENTRYPOINT ["bi-dashboard"]
