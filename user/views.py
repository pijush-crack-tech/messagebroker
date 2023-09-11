

from fastapi import APIRouter

from user.models import User
from user.schema import CreateUser

router = APIRouter()

@router.get("/users")
async def get_user():
    return list(User.all())

@router.post("/create")
async def create_user(user : CreateUser):
    id = User.objects.create(
        name = user.name,
        mobile = user.mobile
    )
    return {"id" : id}
