"""
Test Script for SafeLink Lite URL Checker
Demonstrates various URL security checks with example URLs
"""

from utils.url_checker import URLChecker

def test_url_checker():
    """Test the URL checker with various examples"""
    
    checker = URLChecker()
    
    # Test URLs with different risk levels
    test_urls = [
        # Safe URLs
        "https://www.google.com",
        "https://github.com/microsoft/vscode",
        "https://stackoverflow.com/questions/tagged/python",
        
        # Suspicious URLs
        "http://example.com",  # No HTTPS
        "https://bit.ly/3abc123",  # URL shortener
        "https://sub1.sub2.sub3.example.com",  # Multiple subdomains
        
        # Fraudulent URLs
        "http://192.168.1.1/login",  # IP + suspicious keyword
        "https://secure-paypal-verify-account.fake-site.com",  # Multiple suspicious keywords
        "http://login.bank.update.confirm.urgent.winner.click.here.very.long.malicious.site.com/verify-account-suspended",  # Multiple issues
        
        # Invalid URLs
        "not-a-url",
        "htp://missing-t.com",
        ""
    ]
    
    print("SafeLink Lite - URL Security Test Results")
    print("=" * 50)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. Testing: {url}")
        print("-" * 40)
        
        result = checker.check_url_safety(url)
        
        # Display results
        status_symbols = {
            'SAFE': '[SAFE]',
            'SUSPICIOUS': '[WARN]',
            'FRAUD': '[DANGER]',
            'INVALID': '[ERROR]'
        }
        
        symbol = status_symbols.get(result['status'], '[UNKNOWN]')
        
        print(f"Status: {symbol} {result['status']}")
        print(f"Risk Level: {result['risk_level']}")
        
        if 'risk_score' in result:
            print(f"Risk Score: {result['risk_score']}")
        
        print("Reasons:")
        for reason in result['reasons']:
            print(f"  - {reason}")

if __name__ == "__main__":
    test_url_checker()