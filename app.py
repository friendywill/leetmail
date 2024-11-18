# app.py
import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import httpx
import asyncio
from resend import Resend
import yaml
import secrets

# Initialize FastAPI app
app = FastAPI(title="LeetCode Buddy System")
security = HTTPBasic()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load config from YAML
def load_config():
    if os.path.exists("config.yml"):
        with open("config.yml", "r") as f:
            return yaml.safe_load(f)
    return {"users": []}


def save_config(config):
    with open("config.yml", "w") as f:
        yaml.dump(config, f)


# Models
class User(BaseModel):
    leetcode_username: str
    email: EmailStr


class UserProgress(BaseModel):
    username: str
    solved_count: int
    recent_problems: List[str]
    current_streak: int


# API client for LeetCode
class LeetCodeClient:
    def __init__(self):
        self.base_url = "https://alfa-leetcode-api.onrender.com"

    async def get_user_profile(self, username: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/userProfile/{username}")
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="LeetCode user not found")
            return response.json()

    async def get_user_calendar(self, username: str) -> dict:
        year = datetime.now().year
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/userProfileCalendar",
                params={"username": username, "year": year},
            )
            return response.json()


# Initialize clients
leetcode_client = LeetCodeClient()
resend_client = Resend(api_key=os.getenv("RESEND_API_KEY"))


# Security check for cron endpoint
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("CRON_USERNAME", "admin")
    correct_password = os.getenv("CRON_PASSWORD", "admin")
    is_correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), correct_username.encode("utf8")
    )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), correct_password.encode("utf8")
    )

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


# API Routes
@app.get("/users")
async def get_users():
    config = load_config()
    return config["users"]


@app.post("/users")
async def add_user(user: User):
    config = load_config()
    config["users"].append(user.dict())
    save_config(config)
    return {"message": "User added successfully"}


@app.get("/progress")
async def get_progress() -> List[UserProgress]:
    config = load_config()
    progress_list = []

    for user in config["users"]:
        profile = await leetcode_client.get_user_profile(user["leetcode_username"])
        calendar = await leetcode_client.get_user_calendar(user["leetcode_username"])

        progress = UserProgress(
            username=user["leetcode_username"],
            solved_count=profile.get("totalSolved", 0),
            recent_problems=profile.get("recentSubmissionList", [])[:5],
            current_streak=calendar.get("streak", 0),
        )
        progress_list.append(progress)

    return progress_list


@app.post("/trigger-update")
async def trigger_update(
    credentials: HTTPBasicCredentials = Security(verify_credentials),
):
    progress_list = await get_progress()

    # Create email content
    email_content = "LeetCode Progress Update\n\n"
    for progress in progress_list:
        email_content += f"User: {progress.username}\n"
        email_content += f"Problems Solved: {progress.solved_count}\n"
        email_content += f"Current Streak: {progress.current_streak} days\n"
        email_content += "Recent Problems:\n"
        for problem in progress.recent_problems:
            email_content += f"- {problem}\n"
        email_content += "\n"

    # Send email to all users
    config = load_config()
    for user in config["users"]:
        try:
            resend_client.emails.send(
                {
                    "from": "accountability@leetcodebuddy.com",
                    "to": user["email"],
                    "subject": "LeetCode Progress Update",
                    "text": email_content,
                }
            )
        except Exception as e:
            print(f"Failed to send email to {user['email']}: {str(e)}")

    return {"message": "Update triggered and emails sent"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
