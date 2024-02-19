FROM python:3.12.1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variable
ENV VALID_API_KEYS = "123456789"

EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "main.py"]
