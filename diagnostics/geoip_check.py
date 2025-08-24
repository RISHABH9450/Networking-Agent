"""GeoIP provider via free HTTP API. Replace provider base URL as needed."""
from typing import Dict, Any
import httpx
import socket
from .dns_check import normalize_target

def geoip_lookup(target: str) -> Dict[str, Any]:
    """Perform GeoIP lookup for a target domain/IP"""
    host = normalize_target(target)
    try:
        ip = socket.gethostbyname(host)
    except Exception as e:
        return {"ok": False, "host": host, "error": f"dns_failed: {e}"}

    # Using ipapi.co (no key for basic fields). You can switch to ipinfo.io etc.
    url = f"https://ipapi.co/{ip}/json/"
    try:
        with httpx.Client(timeout=5) as c:
            r = c.get(url)
            data = r.json()
        return {
            "ok": True,
            "host": host,
            "ip": ip,
            "country": data.get("country_name"),
            "region": data.get("region"),
            "city": data.get("city"),
            "asn": data.get("asn"),
            "org": data.get("org"),
            "provider": "ipapi.co",
        }
    except Exception as e:
        return {"ok": False, "host": host, "ip": ip, "error": str(e)}
