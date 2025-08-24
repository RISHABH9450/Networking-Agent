import ssl
import socket
from datetime import datetime, timezone
from typing import Dict, Any
from .dns_check import normalize_target

def ssl_certificate_check(target: str) -> Dict[str, Any]:
    """Check SSL certificate validity and expiration for a target"""
    host = normalize_target(target)
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
        
        not_after = cert.get("notAfter") if cert else None
        expires_at = None
        days_left = None
        
        if isinstance(not_after, str):
            expires_at = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            days_left = (expires_at - datetime.now(timezone.utc)).days
        
        subj = {k: v for x in cert.get("subject", []) for k, v in x} if cert else {}
        issr = {k: v for x in cert.get("issuer", []) for k, v in x} if cert else {}
        
        return {
            "ok": days_left is None or days_left > 0,
            "host": host,
            "subject": subj,
            "issuer": issr,
            "expires_at": expires_at.isoformat() if expires_at else None,
            "days_left": days_left,
        }
    except Exception as e:
        return {"ok": False, "host": host, "error": str(e)}
