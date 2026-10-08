import logging
import sys

from exception import BaseException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from route import router as app_router

logging.basicConfig(
    level=logging.INFO,
    format="- %(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
        
    ]
)



app= FastAPI(
    title= "PyTest unit testing",
    version= "1.0",
    description= "This is solely for learning purpose, to understand how unit test works",
    debug=False
    
    
)

app.include_router(app_router, tags=["App router"])


@app.exception_handler(BaseException)
async def app_exception_handler(request: Request, exc: BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.msg,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code= 500,
        content={
            "error": True,
            "msg":"Something went wrong, try again later."
        }
    )

