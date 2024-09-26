FROM python:3.10

# Install Xvfb and other dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

COPY img /app/img

# Command to run your application with Xvfb
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & DISPLAY=:99 python main.py"]
