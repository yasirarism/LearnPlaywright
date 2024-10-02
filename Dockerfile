# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    xvfb

# Add Google Chrome’s signing key
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -

# Set up the Chrome repository
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/

# Install selenium
RUN pip install -r requirements.txt

# Set environment variable for Chrome binary location
ENV CHROME_BIN=/usr/bin/google-chrome

# Set environment variable for ChromeDriver location
ENV CHROMEDRIVER=/usr/local/bin/chromedriver

# Add a simple script or app to run (if needed)
CMD ["python3", "runapi.py"]
