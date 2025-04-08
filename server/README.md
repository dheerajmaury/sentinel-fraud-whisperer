
# Sentinel Fraud Detection API

This directory contains the FastAPI server for the Sentinel Fraud Detection system.

## Setup Instructions

1. Make sure you have Python 3.7+ installed

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the server:
   ```
   python run.py
   ```

The server will start on http://localhost:8000 by default.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Environment Variables

Environment variables can be configured in the `.env` file:
- `PORT`: Server port (default: 8000)
- `HOST`: Host address (default: 0.0.0.0)
