from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
from datetime import datetime, timedelta
import os
import secrets
from typing import Optional
from pydantic import BaseModel, EmailStr
import emails
from jose import jwt

app = FastAPI(title="Passwordless Auth API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class EmailSchema(BaseModel):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

def send_login_email(email: str, token: str):
    """Send login email with magic link."""
    message = emails.Message(
        subject="Your Magic Login Link",
        html=f"""
        <h1>Click the link below to login:</h1>
        <p><a href="http://localhost:8000/verify?token={token}">Login to your account</a></p>
        <p>This link will expire in 10 minutes.</p>
        """,
        mail_from="noreply@yourdomain.com"
    )
    
    # For development, just print the token
    print(f"Magic link token for {email}: {token}")
    # In production, uncomment this to actually send emails
    # message.send(to=email)

@app.post("/request-login")
async def request_login(email_data: EmailSchema):
    """Request a magic link login."""
    email = email_data.email
    # Generate a random token
    token = secrets.token_urlsafe(32)
    
    # Store the token in Redis with 10 minutes expiration
    redis_client.setex(f"login_token:{token}", 600, email)
    
    # Send the magic link email
    send_login_email(email, token)
    
    return {"message": "Magic link sent to your email"}

@app.get("/verify")
async def verify_token(token: str):
    """Verify the magic link token and create a session."""
    # Get email from Redis using token
    redis_key = f"login_token:{token}"
    email = redis_client.get(redis_key)
    
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Delete the token from Redis
    redis_client.delete(redis_key)
    
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/protected")
async def protected_route(request: Request):
    """Example protected route."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"message": f"Hello {email}! This is a protected route."}
