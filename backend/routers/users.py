from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/api", tags=["users"])

# Predefined users as per PRD
PREDEFINED_USERS = [
    "Krishna",
    "Abhishek",
    "Naveen",
    "Pranav",
    "Devashri",
    "Abhinav",
    "Stanzin",
    "Ganadhitya",
    "Manasa",
    "Sathwik",
    "Prasidhvel",
    "Swati",
    "Murali",
    "Nitesh",
    "Mohana Krishna"
]


@router.get("/users")
async def get_users() -> dict:
    """
    Get list of predefined users.
    
    Returns:
        Dictionary containing list of usernames
    """
    return {"users": PREDEFINED_USERS}
