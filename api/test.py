def handler(request):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>SafeLink Premium - Test</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                    margin: 0;
                }
                .container { 
                    max-width: 800px; 
                    margin: 0 auto;
                    background: rgba(255,255,255,0.1);
                    padding: 40px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }
                h1 { font-size: 3rem; margin-bottom: 20px; }
                p { font-size: 1.2rem; opacity: 0.9; }
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
                    <h3>✅ Vercel Serverless Function Working!</h3>
                    <p>Basic handler test successful!</p>
                    <p>No Flask, no imports, pure serverless function.</p>
                </div>
                <p><strong>Next Step:</strong> Add Flask functionality step by step.</p>
            </div>
        </body>
        </html>
        '''
    }
