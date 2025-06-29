# Use a lightweight Python image
FROM python:3.11-slim

# set working dir
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy in your script
COPY bambu_bridge.py .

# run the script
CMD ["python", "bambu_bridge.py"]