import time
import uuid
from dataclasses import dataclass, asdict
from fastapi import  FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .caption import caption_router
from .models import model


@dataclass
class AppConfig:
    version: str = "v1.0"
    prefix: str = ""
    title: str = "musuem_api"
    description: str = "musuem_api_recommend"


app = FastAPI(**asdict(AppConfig()))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_trace_code_header(request: Request, call_next):
    """uuid를 trace code로 발급"""
    trace_code = str(uuid.uuid4())
    request.state.trace_code = trace_code
    response = await call_next(request)
    response.headers["X-Trace-Code"] = trace_code
    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """api 처리시간"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(RequestValidationError)
async def unicorn_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors(),  # Includes detailed validation errors
            "body": exc.body  # Optionally return the request body if needed
        },
    )

app.include_router(caption_router.router)