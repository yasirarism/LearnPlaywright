# Use a Python base image compatible with ARM architecture
FROM python:3.9-slim

# Install Chrome browser, Cloudflare Warp CLI, and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    lsb-release \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && curl https://pkg.cloudflareclient.com/pubkey.gpg | apt-key add - \
    && echo "deb https://pkg.cloudflareclient.com/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/cloudflare-client.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    cloudflare-warp \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install the appropriate ChromeDriver (x86_64 version)
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip -d /usr/local/bin \
    && rm chromedriver-linux64.zip

# Make sure chromedriver is executable
RUN chmod +x /usr/local/bin/chromedriver-linux64/chromedriver

# Add Chrome and ChromeDriver to PATH
ENV PATH="/usr/local/chrome-linux-arm64:$PATH"
ENV PATH="/usr/local/bin/chromedriver-linux64:$PATH"

# Configure Cloudflare Warp
RUN warp-cli register \
    && warp-cli connect \
    && warp-cli enable-always-on

# Copy application code
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Verify installations
RUN which google-chrome && google-chrome --version
RUN which chromedriver && chromedriver --version
RUN warp-cli status

# Command to run your application
CMD ["python3", "runapi.py"]
