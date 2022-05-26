FROM python:3.9

ARG PORT

# Copy the code
WORKDIR /code

# Copy all re dependencies
COPY ./requirements.txt /code/requirements.txt

# Install all the requirements without caching
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy code
COPY ./app /code/app

# Run an app
CMD uvicorn app:create_app --host 0.0.0.0 --port $MONGO_SERVICE_APP_PORT