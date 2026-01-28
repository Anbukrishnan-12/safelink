from flask import Flask, request, jsonify, render_template
from utils.url_checker import URLChecker
from utils.company_verifier import CompanyVerifier

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

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
    try:
        data = request.get_json()
        company_name = data.get('company_name', '')
        
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        result = company_verifier.verify_company(company_name)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

# Vercel serverless function handler
def handler(request):
    return app(request.environ, start_response)
