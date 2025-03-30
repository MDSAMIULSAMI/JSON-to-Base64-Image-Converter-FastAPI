# Use an official Python image with Debian (so we can install Tesseract)
FROM python:3.9

# Install system dependencies, including Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Set working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the Tesseract path
ENV TESSERACT_CMD=/usr/bin/tesseract

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]