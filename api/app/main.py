from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.routes import urls, health
from app.database import engine, Base

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener", description="Production-grade URL shortener", version="1.0.0"
)

# CORS — allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in prod!
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-register Prometheus metrics at /metrics
Instrumentator().instrument(app).expose(app)

# Register route groups
app.include_router(urls.router, prefix="/api/v1")
app.include_router(health.router)
