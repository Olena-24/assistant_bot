# Use a base image with Python 3.12
FROM python:3.12.0-slim

# Install poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy only the files necessary for installing dependencies to avoid cache invalidation
COPY pyproject.toml poetry.lock* /app/

# Disable the creation of virtual environments and install dependencies
# Ensure no interaction and no ANSI output for cleaner logs
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of your application code
COPY . /app

# Command to run your application
CMD ["python", "main.py"]