from fastapi import FastAPI
from .routers import data, health # Import the routers
app = FastAPI(
    title="PorQua Web API",
    description="RESTful API for interacting with the PorQua portfolio optimization library.",
    version="0.1.0"
)

app.include_router(health.router)
app.include_router(data.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PorQua Web API! Visit /docs for documentation."} 