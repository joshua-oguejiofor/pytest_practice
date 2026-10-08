import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)



class LoggingMiddleware(BaseHTTPMiddleware):
    
    async def logging_config(request: Request, call_next):
        
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        
        logger.info(
            "%s %s status=%s duration=%.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
        
        
        return response
        
    
    

