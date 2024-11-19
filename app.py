# app.py
import os
from jsonschema import validate
from config import settings
from leet_logger import logger_runs, logger_main
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import httpx
import resend
import yaml
import secrets

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "users": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "leetcode_username": {"type": "string"},
                    "email": {
                        "type": "string",
                        "format": "email"  # Ensures valid email format
                    },
                },
                "required": ["leetcode_username", "email"],  # Ensure both fields are present
            },
        },
    },
    "required": ["users"],  # Ensure "users" key is present
    "additionalProperties": False,  # Disallow any unexpected keys at the root level
}

# Initialize FastAPI app
app = FastAPI(title="Leetmail ✉️ 🚀")
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
def load_config() -> dict[str, list[dict[str, str]]]:
    is_nested_key_str = False
    is_nested_value_str = False
    is_dict_list = False
    is_list_dict = False
    if os.path.exists("config.yml"):
        with open("config.yml", "r") as f:
            data = yaml.safe_load(f) # pyright: ignore[reportAny]
            validate(data, CONFIG_SCHEMA) # pyright: ignore[reportAny]
            return data # pyright: ignore[reportAny]
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
    recent_problems: list[str]
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
resend.api_key = settings.RESEND_API_KEY


# Security check for cron endpoint
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    is_correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), settings.CRON_USERNAME.encode("utf8")
    )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), settings.CRON_PASSWORD.encode("utf8")
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
async def get_progress() -> list[UserProgress]:
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
            params: resend.Emails.SendParams = {
                "from": settings.FROM_EMAIL,
                "to": [user["email"]],
                "subject": settings.EMAIL_SUBJECT,
                "text": email_content,
            }
            email = resend.Emails.send(params)
            print(f"Email sent successfully: {email}")
        except Exception as e:
            print(f"Failed to send email to {user['email']}: {str(e)}")

    return {"message": "Update triggered and emails sent"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
