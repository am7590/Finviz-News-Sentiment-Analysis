# Set base image (host OS)
FROM --platform=linux/amd64 python:3.10.1
# By default, listen on port 5000
EXPOSE 8080/tcp

# Set the working directory in the container
WORKDIR /main

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip3 install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .
COPY main.py .

# Specify the command to run on container start
CMD [ "python3", "./app.py" ]