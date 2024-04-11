from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # token
    JWT_ALGORITHM: str
    JWT_SECRET: str
    ACCESS_TOKEN_LIFETIME: int

    class Config:
        env_file = ".env"
        extra = "ignore"


project_settings = Settings()
