from typing import Dict, Any
from ping3 import ping  # type: ignore
from .dns_check import normalize_target

def ping_host(target: str) -> Dict[str, Any]:
    """Perform ping connectivity test to a target host"""
    host = normalize_target(target)
    try:
        rtt = ping(host, timeout=2)
        if rtt is None:
            return {"ok": False, "host": host, "latency_ms": None, "error": "timeout"}
        return {"ok": True, "host": host, "latency_ms": round(rtt * 1000, 2)}
    except Exception as e:
        return {"ok": False, "host": host, "latency_ms": None, "error": str(e)}
