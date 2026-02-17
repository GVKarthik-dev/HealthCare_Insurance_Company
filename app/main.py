from fastapi import FastAPI
from .api.endpoints import router as api_router
import uvicorn

app = FastAPI(title="Medical Claim Processing API")

# Include the API router
app.include_router(api_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "running"}

@app.get("/")
def home():
    return {"message": "Medical Claim Processing API is up and running."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
