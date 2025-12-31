from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import src.models as models
from src.database import engine
from src.routers import users, items, auth
from src.middleware.logging import LoggingMiddleware
from src.middleware.rate_limit import RateLimitMiddleware
from src.middleware.error_handler import ErrorHandlerMiddleware
from src.config import get_settings

settings = get_settings()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="A well-structured FastAPI application with middleware and error handling",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug
)

# Add middleware (order matters - first added is executed last)
# 1. Error handler (catches all errors)
app.add_middleware(ErrorHandlerMiddleware)

# 2. Logging (logs all requests)
app.add_middleware(LoggingMiddleware)

# 3. Rate limiting (limits requests per IP)
app.add_middleware(
    RateLimitMiddleware, 
    requests_per_minute=settings.rate_limit_requests
)

# 4. CORS (allows frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "detail": exc.errors(),
            "body": exc.body
        }
    )

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": "1.0.0",
        "environment": settings.environment,
        "docs": "/docs",
        "redoc": "/redoc",
        "features": [
            "Authentication with JWT",
            "Request logging",
            "Rate limiting",
            "Error handling",
            "CORS support"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-01-01T00:00:00Z"
    }

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    print(f"🚀 {settings.app_name} starting...")
    print(f"🌍 Environment: {settings.environment}")
    print(f"🔧 Debug mode: {settings.debug}")
    print("📚 API docs: http://127.0.0.1:8000/docs")
    print("📖 ReDoc: http://127.0.0.1:8000/redoc")
    print(f"🔒 Rate limit: {settings.rate_limit_requests} requests/{settings.rate_limit_window}s per IP")
    print("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Application shutting down...")