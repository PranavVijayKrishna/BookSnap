from fastapi import APIRouter

router = APIRouter(
    prefix = "/preprocess",
    tags = ["Preprocessing"],
)

@router.get("/test")
def test_preprocess():
    return {"message": "Preprocessing router connected!"}

