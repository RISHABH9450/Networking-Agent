from typing import Any, Dict, Mapping

from diagnostics import dns_check, ssl_check, http_check, ping_check, geoip_check, portia_check
from utils import explain


def run_diagnostics(domain: str, mode: str = "beginner") -> Dict[str, Any]:
    """
    Run all networking diagnostic checks and return both raw and explained results.

    Args:
        domain (str): The domain/URL to test.
        mode (str): "beginner" or "expert" — decides explanation detail.

    Returns:
        dict: {
            "raw": { ... all raw outputs ... },
            "explained": { ... simplified explanations ... },
            "health_score": int,
            "summary": str,
            "fix_suggestions": list
        }
    """

    # Collect raw results
    raw_results: Mapping[str, Any] = {
        "dns": dns_check.dns_resolution(domain),
        "ssl": ssl_check.ssl_certificate_check(domain),
        "http": http_check.http_check(domain),
        "ping": ping_check.ping_host(domain),
        "geoip": geoip_check.geoip_lookup(domain),
    }

    # Explain results in human-friendly format
    explained: Dict[str, Any] = {
        "dns": explain.explain_dns(raw_results["dns"], mode),
        "ssl": explain.explain_ssl(raw_results["ssl"], mode),
        "http": explain.explain_http(raw_results["http"], mode),
        "ping": explain.explain_ping(raw_results["ping"], mode),
        "geoip": explain.explain_geoip(raw_results["geoip"], mode),
    }

    # Calculate health score
    health_score = _calculate_health_score(raw_results)
    
    # Get AI-powered insights from Portia
    ai_insights = portia_check.get_ai_insights(raw_results, domain)
    
    # Generate summary and fix suggestions (enhanced with AI)
    summary, fix_suggestions = _generate_summary_and_fixes(raw_results, domain, ai_insights)

    return {
        "raw": raw_results,
        "explained": explained,
        "health_score": health_score,
        "summary": summary,
        "fix_suggestions": fix_suggestions,
        "ai_insights": ai_insights
    }


def _calculate_health_score(raw_results: Mapping[str, Any]) -> int:
    """Calculate a health score from 0-100 based on diagnostic results"""
    score = 100
    
    # DNS check (25 points)
    if not raw_results["dns"].get("ok", False):
        score -= 25
    
    # HTTP check (25 points)
    if not raw_results["http"].get("ok", False):
        score -= 25
    
    # SSL check (20 points)
    if not raw_results["ssl"].get("ok", False):
        score -= 20
    
    # Ping check (15 points)
    if not raw_results["ping"].get("ok", False):
        score -= 15
    
    # GeoIP check (15 points)
    if not raw_results["geoip"].get("ok", False):
        score -= 15
    
    return max(0, score)


def _generate_summary_and_fixes(raw_results: Mapping[str, Any], domain: str, ai_insights: Dict[str, Any] = None) -> tuple[str, list[str]]:
    """Generate a summary and fix suggestions based on diagnostic results"""
    issues = []
    fixes = []
    
    # Check each diagnostic result
    if not raw_results["dns"].get("ok", False):
        issues.append("DNS resolution failed")
        fixes.append("Check if the domain name is correct and exists")
        fixes.append("Try using a different DNS server (8.8.8.8 or 1.1.1.1)")
    
    if not raw_results["http"].get("ok", False):
        issues.append("HTTP connection failed")
        fixes.append("Verify the website is running and accessible")
        fixes.append("Check if there are any firewall or network restrictions")
    
    if not raw_results["ssl"].get("ok", False):
        issues.append("SSL certificate issues")
        fixes.append("Check SSL certificate validity and expiration")
        fixes.append("Ensure proper SSL configuration on the server")
    
    if not raw_results["ping"].get("ok", False):
        issues.append("Ping connectivity failed")
        fixes.append("Check network connectivity to the target")
        fixes.append("Verify if ICMP traffic is allowed")
    
    if not raw_results["geoip"].get("ok", False):
        issues.append("GeoIP lookup failed")
        fixes.append("This may indicate DNS or connectivity issues")
    
    # Enhance with AI insights if available
    if ai_insights:
        # Add AI-powered intelligent recommendations
        ai_recommendations = ai_insights.get("intelligent_recommendations", [])
        for rec in ai_recommendations:
            ai_fix = f"🤖 {rec.get('action', 'AI Recommendation')}: {rec.get('details', '')}"
            if rec.get('estimated_fix_time'):
                ai_fix += f" (Est. time: {rec['estimated_fix_time']})"
            fixes.append(ai_fix)
        
        # Use AI summary if available
        ai_summary = ai_insights.get("ai_summary", "")
        if ai_summary:
            summary = ai_summary
        elif not issues:
            summary = f"✅ All diagnostics passed for {domain}. The target appears to be healthy and reachable."
        else:
            summary = f"⚠️ Found {len(issues)} issue(s) with {domain}: {', '.join(issues)}"
    else:
        # Generate summary without AI
        if not issues:
            summary = f"✅ All diagnostics passed for {domain}. The target appears to be healthy and reachable."
        else:
            summary = f"⚠️ Found {len(issues)} issue(s) with {domain}: {', '.join(issues)}"
    
    return summary, fixes
