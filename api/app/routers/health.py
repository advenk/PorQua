from fastapi import APIRouter

router = APIRouter(
    tags=["Service Health"],
)

@router.get("/health", summary="Health Check URL")
def health_check():
    """Returns 200 OK status if the API service is running."""
    return {"status": "OK"} 