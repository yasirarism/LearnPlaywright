# Use a Python base image compatible with ARM architecture
FROM python:3.9-slim

# Install Chrome browser and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip -d /usr/local/bin \
    && rm chromedriver-linux64.zip

# Copy application code
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

RUN which chrome && chrome --version
RUN which chromedriver && chromedriver --version

# Command to run your application
CMD ["python3", "runapi.py"]
# CMD ["python3", "async_scraper.py"]
