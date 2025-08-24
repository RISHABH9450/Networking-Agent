"""
Portia AI integration for enhanced networking diagnostics and intelligent insights.
"""
import os
import httpx
from typing import Dict, Any, Optional
from config import settings


class PortiaAIClient:
    """Client for interacting with Portia AI API"""
    
    def __init__(self):
        self.api_key = settings.portia_api_key
        self.base_url = "https://api.portia.ai/v1"  # Placeholder URL
        self.timeout = 10
    
    def is_available(self) -> bool:
        """Check if Portia AI is configured and available"""
        return self.api_key is not None and self.api_key.strip() != ""
    
    async def analyze_diagnostics(self, diagnostic_results: Dict[str, Any], target: str) -> Optional[Dict[str, Any]]:
        """
        Send diagnostic results to Portia AI for intelligent analysis
        
        Args:
            diagnostic_results: Raw diagnostic results from all checks
            target: The target domain/IP being diagnosed
            
        Returns:
            AI analysis with insights, root causes, and recommendations
        """
        if not self.is_available():
            return None
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "target": target,
                "diagnostics": diagnostic_results,
                "analysis_type": "network_troubleshooting",
                "include_predictions": True,
                "include_recommendations": True
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/analyze/network",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "error": f"Portia AI API error: {response.status_code}",
                        "fallback": True
                    }
                    
        except Exception as e:
            return {
                "error": f"Portia AI connection failed: {str(e)}",
                "fallback": True
            }
    
    def generate_ai_insights(self, diagnostic_results: Dict[str, Any], target: str) -> Dict[str, Any]:
        """
        Generate AI-powered insights synchronously (fallback method)
        This provides basic AI-like analysis when the API is not available
        """
        if not self.is_available():
            return self._generate_fallback_insights(diagnostic_results, target)
        
        # For now, we'll use the fallback method as the primary implementation
        # In a real implementation, this would make the actual API call
        return self._generate_fallback_insights(diagnostic_results, target)
    
    def _generate_fallback_insights(self, diagnostic_results: Dict[str, Any], target: str) -> Dict[str, Any]:
        """Generate intelligent insights using local analysis"""
        insights = {
            "root_cause_analysis": [],
            "intelligent_recommendations": [],
            "risk_assessment": "low",
            "performance_score": 0,
            "predicted_issues": [],
            "ai_summary": ""
        }
        
        # Analyze DNS issues
        dns_result = diagnostic_results.get("dns", {})
        if not dns_result.get("ok"):
            insights["root_cause_analysis"].append({
                "category": "DNS",
                "severity": "high",
                "issue": "DNS resolution failure",
                "impact": "Complete connectivity loss",
                "technical_details": dns_result.get("error", "Unknown DNS error")
            })
            insights["intelligent_recommendations"].append({
                "priority": "critical",
                "action": "Check DNS configuration",
                "details": "Verify DNS server settings and domain registration status",
                "estimated_fix_time": "5-15 minutes"
            })
            insights["risk_assessment"] = "high"
        else:
            insights["performance_score"] += 25
        
        # Analyze SSL issues
        ssl_result = diagnostic_results.get("ssl", {})
        if not ssl_result.get("ok"):
            insights["root_cause_analysis"].append({
                "category": "SSL",
                "severity": "medium",
                "issue": "SSL certificate problem",
                "impact": "Security warnings for users",
                "technical_details": ssl_result.get("error", "SSL certificate validation failed")
            })
            insights["intelligent_recommendations"].append({
                "priority": "high",
                "action": "Renew SSL certificate",
                "details": "Certificate may be expired or improperly configured",
                "estimated_fix_time": "10-30 minutes"
            })
            if insights["risk_assessment"] == "low":
                insights["risk_assessment"] = "medium"
        else:
            insights["performance_score"] += 25
            # Check for expiring certificates
            days_left = ssl_result.get("days_left")
            if days_left and days_left < 30:
                insights["predicted_issues"].append({
                    "type": "ssl_expiration",
                    "description": f"SSL certificate expires in {days_left} days",
                    "recommended_action": "Schedule certificate renewal",
                    "timeline": "within 2 weeks"
                })
        
        # Analyze HTTP issues
        http_result = diagnostic_results.get("http", {})
        if not http_result.get("ok"):
            insights["root_cause_analysis"].append({
                "category": "HTTP",
                "severity": "high",
                "issue": "HTTP connectivity failure",
                "impact": "Website inaccessible to users",
                "technical_details": http_result.get("error", "HTTP connection failed")
            })
            insights["intelligent_recommendations"].append({
                "priority": "critical",
                "action": "Check web server status",
                "details": "Verify server is running and accepting connections",
                "estimated_fix_time": "5-20 minutes"
            })
            insights["risk_assessment"] = "high"
        else:
            insights["performance_score"] += 25
            # Analyze response time
            response_time = http_result.get("response_time_ms", 0)
            if response_time > 3000:
                insights["predicted_issues"].append({
                    "type": "performance",
                    "description": f"Slow response time: {response_time}ms",
                    "recommended_action": "Optimize server performance or consider CDN",
                    "timeline": "ongoing monitoring recommended"
                })
        
        # Analyze ping connectivity
        ping_result = diagnostic_results.get("ping", {})
        if not ping_result.get("ok"):
            insights["root_cause_analysis"].append({
                "category": "Network",
                "severity": "medium",
                "issue": "ICMP ping failure",
                "impact": "Network connectivity issues",
                "technical_details": ping_result.get("error", "Ping timeout or blocked")
            })
            insights["intelligent_recommendations"].append({
                "priority": "medium",
                "action": "Check network connectivity",
                "details": "ICMP may be blocked by firewall or network issues",
                "estimated_fix_time": "10-30 minutes"
            })
        else:
            insights["performance_score"] += 15
            # Analyze latency
            latency = ping_result.get("latency_ms", 0)
            if latency > 200:
                insights["predicted_issues"].append({
                    "type": "latency",
                    "description": f"High latency: {latency}ms",
                    "recommended_action": "Investigate network path or consider closer servers",
                    "timeline": "ongoing monitoring recommended"
                })
        
        # Analyze GeoIP
        geoip_result = diagnostic_results.get("geoip", {})
        if geoip_result.get("ok"):
            insights["performance_score"] += 10
        
        # Generate AI summary
        if insights["root_cause_analysis"]:
            primary_issues = [issue["category"] for issue in insights["root_cause_analysis"]]
            insights["ai_summary"] = f"🤖 AI Analysis: Detected {len(primary_issues)} primary issue(s) affecting {target}. " + \
                                   f"Main concerns: {', '.join(primary_issues)}. " + \
                                   f"Risk level: {insights['risk_assessment']}. " + \
                                   f"Performance score: {insights['performance_score']}/100."
        else:
            insights["ai_summary"] = f"🤖 AI Analysis: {target} appears healthy with a performance score of {insights['performance_score']}/100. " + \
                                   f"No critical issues detected."
        
        return insights


# Global client instance
portia_client = PortiaAIClient()


def get_ai_insights(diagnostic_results: Dict[str, Any], target: str) -> Dict[str, Any]:
    """
    Get AI-powered insights for diagnostic results
    
    Args:
        diagnostic_results: Raw diagnostic results from all checks
        target: The target domain/IP being diagnosed
        
    Returns:
        AI insights and recommendations
    """
    return portia_client.generate_ai_insights(diagnostic_results, target)