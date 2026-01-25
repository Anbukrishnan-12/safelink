# SafeLink Lite - URL Security Checker

A beginner-friendly Flask web application that analyzes URLs for potential security threats and classifies them as SAFE, SUSPICIOUS, or FRAUD.

## 🎯 Project Overview

SafeLink Lite helps users identify potentially dangerous URLs by performing various security checks without relying on external APIs or machine learning. It uses rule-based analysis to detect common phishing and fraud patterns.

## 🏗️ Project Structure

```
safelink/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   └── style.css         # CSS styling
└── utils/
    └── url_checker.py    # URL security analysis logic
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation & Setup

1. **Navigate to project directory:**
```bash
cd safelink
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python app.py
```

4. **Open your browser and visit:**
```
http://127.0.0.1:5000
```

## 🔍 Security Checks Explained

### 1. URL Format Validation
- **What it checks:** Basic URL structure and syntax
- **Why it matters:** Malformed URLs can indicate malicious intent
- **Example:** `htp://example.com` (missing 't' in 'http')

### 2. HTTPS Encryption Check
- **What it checks:** Whether the URL uses HTTPS protocol
- **Why it matters:** HTTP connections are unencrypted and vulnerable
- **Risk:** +2 points if missing HTTPS

### 3. URL Length Analysis
- **What it checks:** URLs longer than 100 characters
- **Why it matters:** Attackers often use very long URLs to hide malicious domains
- **Risk:** +1 point for excessive length

### 4. IP Address Detection
- **What it checks:** Direct IP addresses instead of domain names
- **Why it matters:** Legitimate sites use domain names, not raw IPs
- **Risk:** +3 points for IP usage
- **Example:** `http://192.168.1.1/login` vs `https://bank.com/login`

### 5. Suspicious Keywords
- **What it checks:** Common phishing terms in URLs
- **Keywords monitored:** login, verify, bank, secure, update, confirm, account, suspended, urgent, paypal, amazon, microsoft, google, apple
- **Why it matters:** Phishers often use these words to create urgency
- **Risk:** +1 point per suspicious keyword

### 6. URL Shortener Detection
- **What it checks:** Known URL shortening services
- **Services detected:** bit.ly, tinyurl.com, t.co, goo.gl, ow.ly, etc.
- **Why it matters:** Shortened URLs hide the real destination
- **Risk:** +2 points for shortened URLs

### 7. Multiple Subdomains
- **What it checks:** Excessive subdomain usage
- **Why it matters:** Attackers use subdomains to mimic legitimate sites
- **Risk:** +2 points for suspicious subdomain patterns
- **Example:** `secure.login.paypal.fake-site.com`

## 📊 Risk Scoring System

| Risk Score | Classification | Risk Level |
|------------|---------------|------------|
| 0          | SAFE          | LOW        |
| 1-3        | SUSPICIOUS    | MEDIUM     |
| 4+         | FRAUD         | HIGH       |

## 🧪 Testing Examples

### Safe URLs
```
https://www.google.com
https://github.com/user/repo
https://stackoverflow.com/questions
```

### Suspicious URLs
```
http://example.com (no HTTPS)
https://bit.ly/abc123 (URL shortener)
https://very.long.subdomain.example.com (multiple subdomains)
```

### Fraudulent URLs
```
http://192.168.1.1/login (IP + suspicious keyword)
https://secure-paypal-verify-account-urgent.fake-site.com
http://login.bank.update.confirm.malicious-site.com
```

## 🛡️ Security Features

- **No External Dependencies:** All analysis is done locally
- **Input Validation:** Prevents injection attacks
- **Error Handling:** Graceful handling of invalid inputs
- **Client-Side Validation:** Basic validation before server processing

## 🔧 Customization

### Adding New Suspicious Keywords
Edit `utils/url_checker.py`:
```python
self.suspicious_keywords = [
    'login', 'verify', 'bank',  # existing keywords
    'crypto', 'wallet', 'nft'   # add new keywords
]
```

### Adjusting Risk Scores
Modify the scoring logic in `check_url_safety()` method:
```python
if self._has_https(url):
    risk_score += 1  # Change from 2 to 1
```

### Adding New URL Shorteners
Update the shorteners list:
```python
self.url_shorteners = [
    'bit.ly', 'tinyurl.com',    # existing
    'short.ly', 'tiny.one'      # add new ones
]
```

## 📝 API Usage

### Check URL Endpoint
```bash
POST /check-url
Content-Type: application/json

{
    "url": "https://example.com"
}
```

### Response Format
```json
{
    "status": "SAFE|SUSPICIOUS|FRAUD",
    "risk_level": "LOW|MEDIUM|HIGH",
    "reasons": ["List of reasons"],
    "risk_score": 0,
    "url": "https://example.com"
}
```

## 🚨 Limitations

- **No Real-time Threat Intelligence:** Doesn't check against live threat databases
- **Rule-based Only:** No machine learning or AI analysis
- **No Content Analysis:** Doesn't examine page content, only URLs
- **Local Analysis:** No network-based reputation checking

## 🔮 Future Enhancements

- Domain reputation checking
- Typosquatting detection
- SSL certificate validation
- Real-time blacklist integration
- Machine learning classification
- Browser extension version

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change port in app.py
app.run(debug=True, host='127.0.0.1', port=5001)
```

**Module not found:**
```bash
# Ensure you're in the correct directory
cd safelink
pip install -r requirements.txt
```

**Flask not starting:**
```bash
# Check Python version
python --version
# Should be 3.7+
```

---

**Built with Flask, HTML5, CSS3, and JavaScript** 🚀

**Focus: Cybersecurity Education & Practical Implementation** 🔒