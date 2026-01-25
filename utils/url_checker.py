"""
URL Security Checker Module
Analyzes URLs for potential security threats using various checks
"""

import re
import ipaddress
from urllib.parse import urlparse

class URLChecker:
    def __init__(self):
        # Suspicious keywords that might indicate phishing
        self.suspicious_keywords = [
            'login', 'verify', 'bank', 'secure', 'update', 'confirm',
            'account', 'suspended', 'urgent', 'click', 'winner',
            'paypal', 'amazon', 'microsoft', 'google', 'apple'
        ]
        
        # Known URL shorteners
        self.url_shorteners = [
            'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly',
            'short.link', 'tiny.cc', 'is.gd', 'buff.ly'
        ]
    
    def check_url_safety(self, url):
        """
        Main function to check URL safety
        Returns: dict with status, risk_level, and reasons
        """
        reasons = []
        risk_score = 0
        
        # 1. Basic URL format validation
        if not self._is_valid_url(url):
            return {
                'status': 'INVALID',
                'risk_level': 'HIGH',
                'reasons': ['Invalid URL format']
            }
        
        # 2. Check if HTTPS is present
        if not self._has_https(url):
            reasons.append('No HTTPS encryption')
            risk_score += 2
        
        # 3. Check URL length (very long URLs can be suspicious)
        if self._is_url_too_long(url):
            reasons.append('Unusually long URL')
            risk_score += 1
        
        # 4. Check if URL uses IP address instead of domain
        if self._uses_ip_address(url):
            reasons.append('Uses IP address instead of domain name')
            risk_score += 3
        
        # 5. Check for suspicious keywords
        suspicious_words = self._check_suspicious_keywords(url)
        if suspicious_words:
            reasons.append(f'Contains suspicious keywords: {", ".join(suspicious_words)}')
            risk_score += len(suspicious_words)
        
        # 6. Check if it's a shortened URL
        if self._is_shortened_url(url):
            reasons.append('Uses URL shortening service')
            risk_score += 2
        
        # 7. Check for multiple subdomains (can indicate phishing)
        if self._has_multiple_subdomains(url):
            reasons.append('Has multiple suspicious subdomains')
            risk_score += 2
        
        # Determine final status based on risk score
        if risk_score == 0:
            status = 'SAFE'
            risk_level = 'LOW'
            reasons = ['URL appears to be safe']
        elif risk_score <= 3:
            status = 'SUSPICIOUS'
            risk_level = 'MEDIUM'
        else:
            status = 'FRAUD'
            risk_level = 'HIGH'
        
        return {
            'status': status,
            'risk_level': risk_level,
            'reasons': reasons,
            'risk_score': risk_score
        }
    
    def _is_valid_url(self, url):
        """Check if URL has valid format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _has_https(self, url):
        """Check if URL uses HTTPS"""
        return url.lower().startswith('https://')
    
    def _is_url_too_long(self, url):
        """Check if URL is suspiciously long (over 100 characters)"""
        return len(url) > 100
    
    def _uses_ip_address(self, url):
        """Check if URL uses IP address instead of domain name"""
        try:
            parsed = urlparse(url)
            host = parsed.netloc.split(':')[0]  # Remove port if present
            ipaddress.ip_address(host)
            return True
        except:
            return False
    
    def _check_suspicious_keywords(self, url):
        """Check for suspicious keywords in URL"""
        url_lower = url.lower()
        found_keywords = []
        
        for keyword in self.suspicious_keywords:
            if keyword in url_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _is_shortened_url(self, url):
        """Check if URL uses a known shortening service"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        return any(shortener in domain for shortener in self.url_shorteners)
    
    def _has_multiple_subdomains(self, url):
        """Check for multiple subdomains (potential phishing indicator)"""
        try:
            parsed = urlparse(url)
            domain_parts = parsed.netloc.split('.')
            # If more than 3 parts (like sub.sub.example.com), it's suspicious
            return len(domain_parts) > 3
        except:
            return False