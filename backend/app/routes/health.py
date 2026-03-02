from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Health check da aplicação"""
    return {
        "status": "healthy",
        "message": "API is running"
    }
