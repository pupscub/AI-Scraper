# Base image with Python 3.11.4
FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome Browser and additional dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    fonts-liberation \
    xdg-utils \
    --no-install-recommends && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install WebDriver Manager to manage ChromeDriver
RUN pip install webdriver-manager

# Set environment variables for Chrome in headless mode
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_DRIVER=/usr/local/bin/chromedriver

# Copy the entire project into the container
COPY . .

# Expose the port that Streamlit will use
EXPOSE 8501

# Clean up any unnecessary packages after installation
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure all packages are updated to their latest versions
RUN apt-get update && apt-get dist-upgrade -y 


# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py"]
