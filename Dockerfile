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
    echo "deb http://pkg.cloudflareclient.com/ focal main" | tee /etc/apt/sources.list.d/cloudflare-client.list

# Set environment variables
ENV DBUS_SESSION_BUS_ADDRESS=none
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install Cloudflare Warp
RUN apt-get update && apt-get install -y cloudflare-warp

# Start warp-svc in the background and check its status
# RUN warp-svc \
#     sleep 2 && \
#     warp-cli --accept-tos registration new && \
#     warp-cli --accept-tos mode warp && \
#     warp-cli --accept-tos connect && \
#     warp-cli --accept-tos status

# Copy application code
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8081

# Debug: Check Chromium and Cloudflare setup
RUN which chromium && chromium --version
RUN which chromedriver && chromedriver --version
RUN curl https://www.cloudflare.com/cdn-cgi/trace

# Command to run your application
CMD ["/bin/bash", "python3 runapi.py"]
