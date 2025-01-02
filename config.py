from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API Keys
    RESEND_API_KEY: str = Field(default="")  # Empty string as default

    # Authentication
    CRON_USERNAME: str = Field(default="admin")
    CRON_PASSWORD: str = Field(default="")  # Empty string as default

    # Email Settings
    FROM_EMAIL: EmailStr = Field(default="updates@leetmail.com")
    EMAIL_SUBJECT: str = Field(
        default="LeetCode: Your Daily LeetCode Progress Update"
    )

    # Server Settings
    PORT: int = Field(default=8000)
    HOST: str = Field(default="0.0.0.0")
    LOG_LEVEL: str = Field(default="INFO")

    # WARN: This is what is shown in the docs, and the pyright LSP is showing the
    # below issue, there does not seem to be another way of doing this without
    # breaking something else.
    model_config = SettingsConfigDict( # pyright: ignore[reportUnannotatedClassAttribute]
        env_file=".env", case_sensitive=True
    )

settings = Settings()
