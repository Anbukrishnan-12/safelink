def handler(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SafeLink Premium</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                max-width: 600px;
                border: 1px solid rgba(255,255,255,0.2);
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 20px;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            }
            p {
                font-size: 1.2rem;
                opacity: 0.9;
                line-height: 1.6;
            }
            .success {
                background: rgba(0,255,0,0.2);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                border: 1px solid rgba(0,255,0,0.3);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔒 SafeLink Premium</h1>
            <p>Advanced URL Safety Checker with Company Verification</p>
            <div class="success">
                <h3>✅ SUCCESS!</h3>
                <p>Serverless function is working perfectly!</p>
                <p>SafeLink Premium is live on Vercel!</p>
            </div>
            <p><strong>Status:</strong> Ready for full features</p>
            <p><strong>Next:</strong> Add URL checking & company verification</p>
        </div>
    </body>
    </html>
    """
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8',
        },
        'body': html_content
    }
