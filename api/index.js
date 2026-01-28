module.exports = (req, res) => {
  res.setHeader('Content-Type', 'text/html');
  
  const html = `
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
              box-shadow: 0 8px 32px rgba(0,0,0,0.1);
          }
          h1 {
              font-size: 3rem;
              margin-bottom: 20px;
              text-shadow: 0 2px 10px rgba(0,0,0,0.3);
              background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
              background-clip: text;
          }
          p {
              font-size: 1.2rem;
              opacity: 0.9;
              line-height: 1.6;
              margin-bottom: 15px;
          }
          .success {
              background: rgba(0,255,0,0.2);
              padding: 20px;
              border-radius: 10px;
              margin: 20px 0;
              border: 1px solid rgba(0,255,0,0.3);
              animation: pulse 2s infinite;
          }
          @keyframes pulse {
              0%, 100% { transform: scale(1); }
              50% { transform: scale(1.02); }
          }
          .features {
              background: rgba(255,255,255,0.05);
              padding: 20px;
              border-radius: 10px;
              margin: 20px 0;
              border: 1px solid rgba(255,255,255,0.1);
          }
          .emoji {
              font-size: 2rem;
              margin-bottom: 10px;
          }
      </style>
  </head>
  <body>
      <div class="container">
          <div class="emoji">🔒</div>
          <h1>SafeLink Premium</h1>
          <p>Advanced URL Safety Checker with Company Verification</p>
          
          <div class="success">
              <h3>✅ SUCCESS!</h3>
              <p>Node.js Serverless Function Working!</p>
              <p>SafeLink Premium is Live on Vercel!</p>
          </div>
          
          <div class="features">
              <h3>🚀 Features Ready:</h3>
              <p>🔍 URL Safety Checker</p>
              <p>🏢 Company Verification</p>
              <p>🎨 Premium Glassmorphism UI</p>
              <p>📱 Mobile Responsive Design</p>
          </div>
          
          <p><strong>Status:</strong> Ready for Full Implementation</p>
          <p><strong>Next:</strong> Add Flask Backend Integration</p>
      </div>
  </body>
  </html>
  `;
  
  res.status(200).send(html);
};
