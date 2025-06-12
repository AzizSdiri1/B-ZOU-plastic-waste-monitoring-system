from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from typing import Dict
import secrets
import time
import uvicorn
from routes import auth, image

# Initialize FastAPI app
app = FastAPI()

# Mount static files for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include modular routes
app.include_router(auth.router, prefix="/auth")
app.include_router(image.router, prefix="/image")

# Serve main HTML pages
@app.get("/", response_class=HTMLResponse)
async def get_register():
    with open("templates/register.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    with open("templates/login.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    with open("templates/dashboard.html", "r") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)