# Use the official Python image with the version you need
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required packages and dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libxshmfence1 \
    libnss3 \
    libxcomposite1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Playwright and its dependencies
RUN pip install playwright

# Install Playwright browsers
RUN playwright install --with-deps

# Copy the rest of the application code
COPY . .

# Set entry point
ENTRYPOINT ["python", "async_scraper.py"]
