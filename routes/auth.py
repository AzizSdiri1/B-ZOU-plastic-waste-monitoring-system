from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Dict
import secrets
import time
import json
import smtplib
from email.mime.text import MIMEText

router = APIRouter()

# In-memory storage for users and OTPs (replace with database for production)
users: Dict[str, str] = {}  # email: password
otp_store: Dict[str, Dict] = {}  # email: {code, timestamp, attempts}

# Load email configuration from JSON file
with open("email_config.json", "r") as f:
    email_config = json.load(f)

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class OTPRequest(BaseModel):
    email: EmailStr
    code: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Send OTP via email
def send_otp_email(email: str, code: str):
    try:
        msg = MIMEText(f"Your OTP is: {code}\nThis code expires in 5 minutes.")
        msg["Subject"] = "Your OTP Code"
        msg["From"] = f"{email_config['sender_name']} <{email_config['sender_email']}>"
        msg["To"] = email

        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(email_config["sender_email"], email_config["sender_password"])
            server.sendmail(email_config["sender_email"], email, msg.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send OTP email: {str(e)}")

# Generate and send OTP
def generate_otp(email: str):
    if email in otp_store and otp_store[email]["attempts"] >= 5:
        raise HTTPException(status_code=429, detail="Too many attempts. Request a new code.")
    code = str(secrets.randbelow(1000000)).zfill(6)
    otp_store[email] = {"code": code, "timestamp": time.time(), "attempts": 0}
    send_otp_email(email, code)
    return {"message": "OTP sent"}

@router.post("/register")
async def register(data: RegisterRequest):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if data.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    users[data.email] = data.password  # Store password (hash in production)
    return generate_otp(data.email)

@router.post("/verify-register")
async def verify_register(data: OTPRequest):
    if data.email not in otp_store:
        raise HTTPException(status_code=400, detail="No OTP sent")
    otp_data = otp_store[data.email]
    if otp_data["attempts"] >= 5:
        raise HTTPException(status_code=429, detail="Too many attempts. Request a new code.")
    if time.time() - otp_data["timestamp"] > 300:  # 5-minute expiry
        raise HTTPException(status_code=400, detail="OTP expired")
    if otp_data["code"] != data.code:
        otp_data["attempts"] += 1
        raise HTTPException(status_code=400, detail="Invalid OTP")
    del otp_store[data.email]  # Clear OTP after success
    return {"message": "Registration successful", "redirect": "/login"}

@router.post("/resend-otp")
async def resend_otp(email: EmailStr):
    if email not in users and email not in otp_store:
        raise HTTPException(status_code=400, detail="Email not found")
    return generate_otp(email)

@router.post("/login")
async def login(data: LoginRequest):
    if data.email not in users or users[data.email] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return generate_otp(data.email)

@router.post("/verify-login")
async def verify_login(data: OTPRequest):
    if data.email not in otp_store:
        raise HTTPException(status_code=400, detail="No OTP sent")
    otp_data = otp_store[data.email]
    if otp_data["attempts"] >= 5:
        raise HTTPException(status_code=429, detail="Too many attempts. Request a new code.")
    if time.time() - otp_data["timestamp"] > 300:  # 5-minute expiry
        raise HTTPException(status_code=400, detail="OTP expired")
    if otp_data["code"] != data.code:
        otp_data["attempts"] += 1
        raise HTTPException(status_code=400, detail="Invalid OTP")
    del otp_store[data.email]  # Clear OTP after success
    return {"message": "Login successful", "redirect": "/dashboard"}