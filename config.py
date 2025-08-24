import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Networking Troubleshooter Agent")
    app_env: str = os.getenv("APP_ENV", "development")
    version: str = os.getenv("APP_VERSION", "1.0")
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")

    # rate limits
    rate_health: str = os.getenv("RATE_HEALTH", "20/minute")
    rate_diagnose: str = os.getenv("RATE_DIAGNOSE", "10/minute")
    rate_report: str = os.getenv("RATE_REPORT", "6/minute")

    # timeouts
    http_timeout: float = float(os.getenv("HTTP_TIMEOUT", 5))
    ping_timeout: float = float(os.getenv("PING_TIMEOUT", 2))
    ssl_timeout: float = float(os.getenv("SSL_TIMEOUT", 5))
    traceroute_timeout: float = float(os.getenv("TRACEROUTE_TIMEOUT", 20))

    # cache
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    ttl_dns: int = int(os.getenv("TTL_DNS", 300))
    ttl_http: int = int(os.getenv("TTL_HTTP", 60))
    ttl_ssl: int = int(os.getenv("TTL_SSL", 300))
    ttl_geoip: int = int(os.getenv("TTL_GEOIP", 86400))

    # providers
    portia_api_key: str | None = os.getenv("PORTIA_API_KEY")
    geoip_base: str = os.getenv("GEOIP_BASE", "https://ipapi.co")

settings = Settings()
