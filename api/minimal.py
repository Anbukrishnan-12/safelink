from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SafeLink Premium - Test</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; }
            .container { max-width: 800px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔒 SafeLink Premium</h1>
            <p>Advanced URL Safety Checker with Company Verification</p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>✅ Vercel Deployment Working!</h3>
                <p>Serverless function is running successfully.</p>
                <p>Next: Add full functionality step by step.</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/check-url', methods=['POST'])
def check_url():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Simple mock response for now
        return jsonify({
            'url': url,
            'is_safe': True,
            'risk_level': 'Low',
            'reasons': ['Basic check passed']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify-company', methods=['POST'])
def verify_company():
    try:
        data = request.get_json()
        company_name = data.get('company_name', '')
        
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        # Simple mock response for now
        return jsonify({
            'company_name': company_name,
            'verified': True,
            'is_real': True,
            'industry': 'Technology',
            'location': 'Global'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel serverless function handler
def handler(request):
    return app(request.environ, start_response)
