"""
Maps raw diagnostic results to Beginner-friendly and Expert-friendly explanations.
"""

from typing import Dict, Any

def explain_dns(result: Dict[str, Any], mode: str = "beginner") -> str:
    """Explain DNS resolution results"""
    if mode == "beginner":
        if result.get("ok"):
            return f"✅ DNS resolution successful! {result.get('host')} resolves to {result.get('ip')}"
        else:
            return f"❌ DNS resolution failed for {result.get('host')}. {result.get('error', '')}"
    else:
        return f"DNS Query: {result.get('host')} → {result.get('ip', 'FAILED')}, Status: {'OK' if result.get('ok') else 'FAILED'}"

def explain_ssl(result: Dict[str, Any], mode: str = "beginner") -> str:
    """Explain SSL certificate results"""
    if mode == "beginner":
        if result.get("ok"):
            days_left = result.get("days_left")
            if days_left is not None:
                return f"🔒 SSL certificate is valid! Expires in {days_left} days."
            else:
                return "🔒 SSL certificate is valid!"
        else:
            return f"⚠️ SSL certificate issue for {result.get('host')}. {result.get('error', '')}"
    else:
        issuer = result.get('issuer', {})
        return f"SSL Check: Valid={result.get('ok')}, Issuer={issuer.get('organizationName', 'Unknown')}, Days Left={result.get('days_left', 'N/A')}"

def explain_http(result: Dict[str, Any], mode: str = "beginner") -> str:
    """Explain HTTP connectivity results"""
    if mode == "beginner":
        if result.get("ok"):
            return f"🌐 Website is reachable! Status code: {result.get('status_code')} ({result.get('response_time_ms')}ms)"
        else:
            return f"⚠️ Website not reachable. {result.get('error', '')}"
    else:
        return f"HTTP Check: Status={result.get('status_code')}, Response Time={result.get('response_time_ms')}ms, Redirects={len(result.get('redirect_chain', []))}"

def explain_ping(result: Dict[str, Any], mode: str = "beginner") -> str:
    """Explain ping connectivity results"""
    if mode == "beginner":
        if result.get("ok"):
            return f"📶 Ping successful! Latency: {result.get('latency_ms')}ms to {result.get('host')}"
        else:
            return f"❌ Cannot ping {result.get('host')}. {result.get('error', '')}"
    else:
        return f"Ping Check: Host={result.get('host')}, RTT={result.get('latency_ms')}ms, Status={'OK' if result.get('ok') else 'FAILED'}"

def explain_geoip(result: Dict[str, Any], mode: str = "beginner") -> str:
    """Explain GeoIP lookup results"""
    if mode == "beginner":
        if result.get("ok"):
            location = f"{result.get('city', 'Unknown')}, {result.get('country', 'Unknown')}"
            return f"🌍 Server is located in {location}. IP: {result.get('ip')}"
        else:
            return f"❌ GeoIP lookup failed. {result.get('error', '')}"
    else:
        return f"GeoIP: IP={result.get('ip')}, ASN={result.get('asn')}, Location={result.get('country')}/{result.get('city')}, Org={result.get('org')}"
