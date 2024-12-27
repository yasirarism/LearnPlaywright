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

# Create a script to start Warp and the Python app
RUN echo '#!/bin/bash \n\
    curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | apt-key add - && \
    echo "deb http://pkg.cloudflareclient.com/ focal main" | tee /etc/apt/sources.list.d/cloudflare-client.list && \
    apt-get update && apt-get install -y cloudflare-warp \n\
    # Start warp-svc in the background \n\
    warp-svc & \n\
    sleep 2 \n\
    # Run warp-cli commands to connect \n\
    warp-cli --accept-tos registration new \n\
    warp-cli --accept-tos mode warp \n\
    warp-cli --accept-tos connect \n\
    warp-cli --accept-tos status \n\
    # Start your Python application \n\
    python3 runapi.py' > /start.sh

# Make the script executable
RUN chmod +x /start.sh

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

# Use the script to start everything
CMD ["/start.sh"]
