from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def health():
    return {"message": "Sedaro Nano API - running!"}