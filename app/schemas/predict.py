# app/schemas/predict.py
from pydantic import BaseModel, HttpUrl

# Pydantic model for input validation
class URLRequest(BaseModel):
    url: HttpUrl  # Ensures the URL is a valid HTTP/HTTPS URL
