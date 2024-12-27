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

# Enable Cloudflare Warp
RUN (warp-svc &) && \
    sleep 2 && \
    warp-cli --accept-tos registration new && \
    warp-cli --accept-tos mode warp && \
    warp-cli --accept-tos connect && \
    warp-cli status

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy application code
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

EXPOSE 8081

RUN which chromium && chromium --version
RUN which chromedriver && chromedriver --version
RUN curl https://www.cloudflare.com/cdn-cgi/trace

# Command to run your application
CMD ["python3", "runapi.py"]
