# Use a Python base image compatible with ARM architecture
FROM python:3.9-slim

# Install necessary packages, including Chromium, ChromiumDriver, and Cloudflare Warp
RUN apt-get update && apt-get install -y \
    chromium \
    python3-pip \
    xvfb \
    curl \
    && apt-get clean

# Install ChromiumDriver
RUN apt-get update && apt install chromium-driver -y

# Install Cloudflare Warp
RUN curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | apt-key add - && \
    echo "deb http://pkg.cloudflareclient.com/ focal main" | tee /etc/apt/sources.list.d/cloudflare-client.list && \
    apt-get update && apt-get install -y cloudflare-warp

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy application code
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose port 8081
EXPOSE 8081

# Copy entrypoint script to run Warp and the main application
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use entrypoint to run Warp and the application
ENTRYPOINT ["/entrypoint.sh"]

# Install curl for testing
RUN curl https://www.cloudflare.com/cdn-cgi/trace

# Command to run your application (this will be the default if not specified)
CMD ["python3", "runapi.py"]
