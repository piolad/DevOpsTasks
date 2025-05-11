from celery import Celery

import os

# Get Redis URL from environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Set up the Celery app
app = Celery("worker", broker=REDIS_URL)

@app.task
def add(x, y):
    return x + y

# You can define more tasks here later
