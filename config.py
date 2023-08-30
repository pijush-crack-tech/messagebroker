import os
from functools import lru_cache

from pydantic_settings import BaseSettings


abs_path_env = os.path.abspath(".env")


if os.getenv("CQLENG_ALLOW_SCHEMA_MANAGEMENT") is None:
    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

class Settings(BaseSettings):
    PROJ_NAME: str = "Test Project"
    CASSANDRA_HOST: str = "localhost"
    CASSANDRA_PORT: int = 9042
    CASSANDRA_USER: str = "cassandra"
    CASSANDRA_PASS: str = "cassandra"
    CASSANDRA_KEYSPACE: str = "testdb"
    PROFILE_URL:str="http://localhost:8000/api/v1/profile/"
    #redis_url: str = Field(..., env='REDIS_URL')

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()