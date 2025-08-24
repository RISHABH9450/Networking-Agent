import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from agent import run_diagnostics

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "networking-troubleshooter-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    """Main page with diagnostic form"""
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    """Run diagnostics on the provided domain/IP"""
    target = request.form.get('target', '').strip()
    mode = request.form.get('mode', 'beginner')
    
    if not target:
        flash('Please enter a domain or IP address to diagnose.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Run the diagnostic agent
        result = run_diagnostics(target, mode)
        return render_template('results.html', target=target, mode=mode, result=result)
    except Exception as e:
        app.logger.error(f"Diagnostic error for {target}: {str(e)}")
        flash(f'Error running diagnostics: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/diagnose')
def api_diagnose():
    """API endpoint for diagnostics (for potential AJAX usage)"""
    target = request.args.get('url', '').strip()
    mode = request.args.get('mode', 'beginner')
    
    if not target:
        return jsonify({"success": False, "error": "No target provided"})
    
    try:
        result = run_diagnostics(target, mode)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        app.logger.error(f"API diagnostic error for {target}: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Networking Troubleshooter Agent is running 🚀"})

@app.route('/api/ai-insights')
def api_ai_insights():
    """API endpoint specifically for AI insights"""
    target = request.args.get('url', '').strip()
    
    if not target:
        return jsonify({"success": False, "error": "No target provided"})
    
    try:
        # Import here to avoid circular imports
        from diagnostics import portia_check, dns_check, ssl_check, http_check, ping_check, geoip_check
        
        # Run basic diagnostics
        raw_results = {
            "dns": dns_check.dns_resolution(target),
            "ssl": ssl_check.ssl_certificate_check(target),
            "http": http_check.http_check(target),
            "ping": ping_check.ping_host(target),
            "geoip": geoip_check.geoip_lookup(target),
        }
        
        # Get AI insights
        ai_insights = portia_check.get_ai_insights(raw_results, target)
        
        return jsonify({
            "success": True, 
            "ai_insights": ai_insights,
            "portia_available": portia_check.portia_client.is_available()
        })
    except Exception as e:
        app.logger.error(f"AI insights error for {target}: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
