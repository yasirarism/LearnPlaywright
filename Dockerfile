# Use a Python base image compatible with ARM architecture
FROM python:3.9-slim

# Install necessary packages, including Chromium and ChromiumDriver
RUN apt-get update && apt-get install -y \
    chromium \
    python3-pip \
    xvfb \
    && apt-get clean

RUN apt-get update && apt install chromium-driver -y

# Set environment variable for Chromium binary location
ENV CHROME_BIN=/usr/bin/chromium

# Set environment variable for ChromiumDriver location
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy application code
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

RUN which chromium && chromium --version
RUN which chromedriver && chromedriver --version

# Command to run your application
# CMD ["python3", "runapi.py"]
CMD ["python3", "async_scraper.py"]
