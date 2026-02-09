from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from ..core.orchestrator import AIOrchestrator

app = FastAPI(
    title="Todo System API",
    description="API for the Todo System with Agent Skills architecture",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Global orchestrator for background tasks
orchestrator = AIOrchestrator()

@app.get("/")
async def root():
    return {
        "message": "Todo System API",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

@app.on_event("startup")
async def startup_event():
    print("íº€ Todo System API started")

@app.on_event("shutdown")
async def shutdown_event():
    print("í»‘ Todo System API shutting down")
