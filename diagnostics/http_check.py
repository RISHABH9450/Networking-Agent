import time
from typing import Dict, Any
import httpx
from config import settings

def _prepare_url(url: str) -> str:
    """Prepare URL with protocol if missing"""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return f"https://{url}"

def http_check(target: str) -> Dict[str, Any]:
    """Perform HTTP connectivity and response check"""
    url = _prepare_url(target)
    try:
        start = time.perf_counter()
        with httpx.Client(follow_redirects=True, timeout=settings.http_timeout) as c:
            r = c.get(url)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {
            "ok": r.status_code < 400,
            "url": url,
            "status_code": r.status_code,
            "response_time_ms": elapsed_ms,
            "final_url": str(r.url),
            "redirect_chain": [h.status_code for h in r.history],
        }
    except Exception as e:
        return {"ok": False, "url": url, "error": str(e)}
