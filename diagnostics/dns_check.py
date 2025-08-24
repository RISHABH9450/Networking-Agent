import socket
from typing import Dict, Any

def normalize_target(target: str) -> str:
    """Normalize a target URL/domain to just the hostname"""
    if target.startswith("http://") or target.startswith("https://"):
        target = target.split("//", 1)[1]
    return target.split("/", 1)[0]


def dns_resolution(target: str) -> Dict[str, Any]:
    """Perform DNS resolution check on a target domain"""
    host = normalize_target(target)
    try:
        ip = socket.gethostbyname(host)
        return {"ok": True, "host": host, "ip": ip}
    except Exception as e:
        return {"ok": False, "host": host, "error": str(e)}
