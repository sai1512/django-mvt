# Session 7 — Dockerfile for Student Platform
# Place this file in your project root (next to manage.py)

# Step 1: Choose a base image
# Use python:3.12-slim — a lightweight Python image
# Hint: FROM <image>
FROM python:3.12-slim


# Step 2: Set the working directory inside the container
# This is where your code will live inside the container
# Hint: WORKDIR /app
WORKDIR /app


# Step 3: Copy requirements.txt and install dependencies
# We copy requirements first so Docker can cache this layer
# If requirements haven't changed, pip install is skipped on rebuild
# Hint: COPY <file> .
# Hint: RUN pip install --no-cache-dir -r <file>
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Step 4: Copy the rest of your project code
# Hint: COPY . .
COPY . .


# Step 5: Tell Docker which port the app uses (documentation only)
# Hint: EXPOSE <port>
EXPOSE 8000


# Step 6: The command to run when the container starts
# Use 0.0.0.0 so the server is accessible from outside the container
# Hint: CMD ["python", "manage.py", "runserver", "<host>:<port>"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
