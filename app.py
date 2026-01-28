"""
SafeLink Lite - URL Security Checker
A Flask web application to check if URLs are safe, suspicious, or fraudulent
"""

from flask import Flask, request, jsonify, render_template
from utils.url_checker import URLChecker
from utils.company_verifier import CompanyVerifier
import os

app = Flask(__name__)

# Initialize checkers
url_checker = URLChecker()
company_verifier = CompanyVerifier()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-url', methods=['POST'])
def check_url():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        result = url_checker.check_url_safety(url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify-company', methods=['POST'])
def verify_company():
    """
    Accepts JSON with 'company_name' field and returns verification details
    """
    try:
        # Get company name from request
        data = request.get_json()
        
        if not data or 'company_name' not in data:
            return jsonify({
                'error': 'Company name is required'
            }), 400
        
        company_name = data['company_name'].strip()
        
        if not company_name:
            return jsonify({
                'error': 'Company name cannot be empty'
            }), 400
        
        # Verify company
        result = company_verifier.verify_company(company_name)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("SafeLink Premium - Advanced URL Security Checker")
    print("Starting server at http://127.0.0.1:5000")
    print("Open your browser and navigate to the URL above")
    
    # Run Flask app in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# Vercel serverless function handler
def handler(request):
    return app(request.environ, start_response)