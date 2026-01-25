"""
SafeLink Lite - URL Security Checker
A Flask web application to check if URLs are safe, suspicious, or fraudulent
"""

from flask import Flask, render_template, request, jsonify
from utils.url_checker import URLChecker
from utils.company_verifier import CompanyVerifier

# Initialize Flask app
app = Flask(__name__)

# Initialize checkers
url_checker = URLChecker()
company_verifier = CompanyVerifier()

@app.route('/')
def home():
    """
    Home page with URL input form
    """
    return render_template('index.html')

@app.route('/check-url', methods=['POST'])
def check_url():
    """
    API endpoint to check URL safety
    Accepts JSON with 'url' field and returns safety analysis
    """
    try:
        # Get URL from request
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL is required'
            }), 400
        
        url = data['url'].strip()
        
        if not url:
            return jsonify({
                'error': 'URL cannot be empty'
            }), 400
        
        # Check URL safety
        result = url_checker.check_url_safety(url)
        
        # Add the original URL to response
        result['url'] = url
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/verify-company', methods=['POST'])
def verify_company():
    """
    API endpoint to verify company information
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
    print("SafeLink Lite - URL Security Checker")
    print("Starting server at http://127.0.0.1:5000")
    print("Open your browser and navigate to the URL above")
    
    # Run Flask app in debug mode for development
    app.run(debug=True, host='127.0.0.1', port=5000)