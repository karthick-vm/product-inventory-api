from fastapi import APIRouter, HTTPException, Depends
from security import hash_password, verify_password, create_access_token
from schemas.auth import UserCreate # , LoginRequest
from models.product import User
from sqlalchemy.orm import Session
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(
        username = user.username,
        password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "User Registered"

@router.post("/login")    # Below form_data we use only for swagger but prefer -> login_data: LoginRequest
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        {"sub":db_user.username}
    )
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }
