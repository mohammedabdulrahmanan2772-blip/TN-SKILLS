from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from legalEaseAPI.routes import router
import config

app = FastAPI(title="LegalEase - AI Legal Document Generator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to LegalEase AI Legal Document Generator API"}

# Run FastAPI if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.BACKEND_HOST, port=config.BACKEND_PORT)
