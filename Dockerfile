# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container (if you have one)
COPY requirements.txt /app/requirements.txt

# Install any dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN apt-get update && apt-get install -y \
python3-tk \
tk-dev

# Copy the rest of the application code to the container
COPY . /app

# Expose the port the application runs on (adjust this to your port, if needed)
EXPOSE 5000

# Run the application (replace `main.py` with the actual entry point of your app)
CMD ["python", "main.py"]
