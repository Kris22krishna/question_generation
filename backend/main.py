from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import users, skills, suggestions, templates, preview

# Create FastAPI application
app = FastAPI(
    title="Dynamic Question Template Builder API",
    description="API for creating and managing dynamic math question templates",
    version="1.0.0"
)

# Configure CORS
# Configure CORS
origins = settings.cors_origins
# Debugging: Ensure localhost:5500 is included
if "http://localhost:5500" not in origins:
    origins.append("http://localhost:5500")

print(f"DEBUG: Loaded CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(skills.router)
app.include_router(suggestions.router)
app.include_router(templates.router)
app.include_router(preview.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Dynamic Question Template Builder API is running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "development"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
