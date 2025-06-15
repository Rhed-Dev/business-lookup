"""
Authentication and rate limiting utilities for FastAPI endpoints.
"""
import time
import logging
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from collections import defaultdict
from src.config import settings

RATE_LIMIT = 100  # requests per minute per API key
WINDOW_SECONDS = 60
rate_limit_store = defaultdict(list)  # {api_key: [timestamps]}

API_KEYS = set([settings.API_KEY])  # Add more keys as needed
logger = logging.getLogger("business_lookup_auth")

security = HTTPBearer()


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency for FastAPI endpoints to verify API key from HTTP Bearer token and enforce rate limiting.
    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token credentials.
    Raises:
        HTTPException: If API key is invalid or rate limit exceeded.
    """
    api_key = credentials.credentials
    if api_key not in API_KEYS:
        logger.warning(f"Unauthorized access attempt with key: {api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    now = time.time()
    window_start = now - WINDOW_SECONDS
    timestamps = rate_limit_store[api_key]
    # Remove timestamps outside the window
    rate_limit_store[api_key] = [ts for ts in timestamps if ts > window_start]
    if len(rate_limit_store[api_key]) >= RATE_LIMIT:
        logger.warning(f"Rate limit exceeded for key: {api_key}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded (100 per minute)")
    rate_limit_store[api_key].append(now)
