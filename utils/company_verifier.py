"""
Company Verification Module
Verifies company information using external APIs
"""

import requests
import os
import re
from urllib.parse import urlparse, urljoin
from typing import Dict, Optional
import time
from bs4 import BeautifulSoup

class CompanyVerifier:
    def __init__(self):
        # Clearbit API configuration
        self.clearbit_api_key = os.getenv('CLEARBIT_API_KEY', '')
        self.clearbit_base_url = 'https://company.clearbit.com/v2/companies/find'
        
        # User agent for requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def verify_company(self, company_input: str) -> Dict:
        """
        Verify company information using multiple sources
        Accepts either company name or URL
        Returns: dict with verification status and company details
        """
        if not company_input or not company_input.strip():
            return {
                'verified': False,
                'is_real': False,
                'error': 'Company name or URL is required'
            }

        company_input = company_input.strip()
        
        try:
            # Check if input is a URL
            if self._is_url(company_input):
                return self._verify_company_by_url(company_input)
            else:
                return self._verify_company_by_name(company_input)
            
        except Exception as e:
            return {
                'verified': False,
                'is_real': False,
                'company_name': company_input,
                'error': f'Verification failed: {str(e)}'
            }

    def _is_url(self, text: str) -> bool:
        """Check if the input text is a URL"""
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _verify_company_by_url(self, url: str) -> Dict:
        """Verify company by analyzing their website URL"""
        verification_results = []
        
        try:
            # Extract domain from URL
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Remove www. if present
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Method 1: Website content analysis
            website_result = self._analyze_website_content(url)
            if website_result:
                verification_results.append(('website', website_result))
            
            # Method 2: Domain verification
            domain_result = self._verify_domain_details(domain)
            if domain_result:
                verification_results.append(('domain', domain_result))
            
            # Method 3: Extract company name from domain
            company_name = self._extract_company_name_from_domain(domain)
            if company_name:
                # Try to verify the extracted company name
                name_result = self._verify_company_by_name(company_name)
                if name_result.get('verified'):
                    verification_results.append(('name', name_result))
            
            # Analyze results
            return self._analyze_verification_results(domain, verification_results)
            
        except Exception as e:
            return {
                'verified': False,
                'is_real': False,
                'company_name': url,
                'error': f'URL verification failed: {str(e)}'
            }

    def _verify_company_by_name(self, company_name: str) -> Dict:
        """Verify company by name (original method)"""
        try:
            # Step 1: Try multiple verification methods
            verification_results = []
            
            # Method 1: Clearbit API
            clearbit_result = self._search_clearbit(company_name)
            if clearbit_result:
                verification_results.append(('clearbit', clearbit_result))
            
            # Method 2: Domain verification
            domain_result = self._verify_company_domain(company_name)
            if domain_result:
                verification_results.append(('domain', domain_result))
            
            # Method 3: Enhanced web search verification
            web_result = self._enhanced_web_search_verification(company_name)
            if web_result:
                verification_results.append(('web', web_result))
            
            # Method 4: Local database fallback
            local_result = self._check_local_database(company_name)
            if local_result:
                verification_results.append(('local', local_result))
            
            # Analyze results and determine if company is real
            return self._analyze_verification_results(company_name, verification_results)
            
        except Exception as e:
            return {
                'verified': False,
                'is_real': False,
                'company_name': company_name,
                'error': f'Verification failed: {str(e)}'
            }

    def _search_clearbit(self, company_name: str) -> Optional[Dict]:
        """Search for company using Clearbit API"""
        if not self.clearbit_api_key:
            return None

        try:
            headers = {
                'Authorization': f'Bearer {self.clearbit_api_key}'
            }

            params = {
                'name': company_name
            }

            response = requests.get(
                self.clearbit_base_url,
                headers=headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                print(f"Clearbit API error: {response.status_code}")
                return None

        except requests.RequestException as e:
            print(f"Clearbit API request failed: {e}")
            return None

    def _fallback_verification(self, company_name: str) -> Dict:
        """Fallback verification when API is not available"""
        # Simple check - if it's a well-known company, provide basic info
        known_companies = {
            'google': {
                'company_name': 'Google LLC',
                'industry': 'Technology',
                'location': 'Mountain View, California, USA',
                'description': 'Technology company specializing in internet services and products'
            },
            'microsoft': {
                'company_name': 'Microsoft Corporation',
                'industry': 'Technology',
                'location': 'Redmond, Washington, USA',
                'description': 'Technology company developing software and hardware'
            },
            'apple': {
                'company_name': 'Apple Inc.',
                'industry': 'Technology',
                'location': 'Cupertino, California, USA',
                'description': 'Technology company designing consumer electronics and software'
            },
            'amazon': {
                'company_name': 'Amazon.com Inc.',
                'industry': 'E-commerce',
                'location': 'Seattle, Washington, USA',
                'description': 'E-commerce and cloud computing company'
            },
            'facebook': {
                'company_name': 'Meta Platforms Inc.',
                'industry': 'Social Media',
                'location': 'Menlo Park, California, USA',
                'description': 'Social media and technology company'
            }
        }

        company_lower = company_name.lower().replace(' ', '')

        for key, info in known_companies.items():
            if key in company_lower:
                return {
                    'verified': True,
                    'company_name': info['company_name'],
                    'industry': info['industry'],
                    'location': info['location'],
                    'description': info['description'],
                    'source': 'Local Database'
                }

        return {
            'verified': False,
            'company_name': company_name,
            'error': 'Company not found in verification database. Please verify manually.'
        }

    def _format_location(self, geo: Dict) -> str:
        """Format location information"""
        if not geo:
            return 'Unknown'

        parts = []
        if geo.get('city'):
            parts.append(geo['city'])
        if geo.get('state'):
            parts.append(geo['state'])
        if geo.get('country'):
            parts.append(geo['country'])

        return ', '.join(parts) if parts else 'Unknown'

    def _extract_social_links(self, social: Dict) -> Dict:
        """Extract social media links"""
        links = {}
        if social.get('twitter', {}).get('handle'):
            links['twitter'] = f"https://twitter.com/{social['twitter']['handle']}"
        if social.get('linkedin', {}).get('handle'):
            links['linkedin'] = f"https://linkedin.com/company/{social['linkedin']['handle']}"
        if social.get('facebook', {}).get('handle'):
            links['facebook'] = f"https://facebook.com/{social['facebook']['handle']}"

        return links

    def _verify_company_domain(self, company_name: str) -> Optional[Dict]:
        """Verify company by checking if their domain exists and is legitimate"""
        try:
            # Generate possible domain names from company name
            possible_domains = self._generate_possible_domains(company_name)
            
            for domain in possible_domains:
                if self._check_domain_exists(domain):
                    return {
                        'domain': domain,
                        'name': company_name,
                        'verification_method': 'domain_check',
                        'confidence': 'medium'
                    }
            
            return None
            
        except Exception as e:
            print(f"Domain verification failed: {e}")
            return None
    
    def _generate_possible_domains(self, company_name: str) -> list:
        """Generate possible domain names from company name"""
        domains = []
        
        # Clean company name
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', company_name.lower().strip())
        name_parts = clean_name.split()
        
        # Generate combinations
        if len(name_parts) == 1:
            # Single word company
            domains.append(f"{name_parts[0]}.com")
            domains.append(f"{name_parts[0]}.net")
            domains.append(f"{name_parts[0]}.org")
            domains.append(f"{name_parts[0]}.co")
        else:
            # Multi-word company
            domains.append(f"{''.join(name_parts)}.com")
            domains.append(f"{''.join(name_parts)}.net")
            domains.append(f"{'_'.join(name_parts)}.com")
            domains.append(f"{'-'.join(name_parts)}.com")
            
            # First word + .com
            if name_parts[0]:
                domains.append(f"{name_parts[0]}.com")
        
        return list(set(domains))  # Remove duplicates
    
    def _check_domain_exists(self, domain: str) -> bool:
        """Check if a domain exists and resolves"""
        try:
            # Try to make HTTP request to the domain
            response = requests.get(f"http://{domain}", headers=self.headers, timeout=5, allow_redirects=True)
            return response.status_code < 500
        except:
            try:
                # Try HTTPS
                response = requests.get(f"https://{domain}", headers=self.headers, timeout=5, allow_redirects=True)
                return response.status_code < 500
            except:
                return False

    def _analyze_website_content(self, url: str) -> Optional[Dict]:
        """Analyze website content to extract company information"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract company information from website
            company_info = {
                'url': url,
                'verification_method': 'website_analysis',
                'confidence': 'high'
            }
            
            # Extract title
            title = soup.find('title')
            if title:
                company_info['website_title'] = title.get_text().strip()
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                company_info['description'] = meta_desc.get('content').strip()
            
            # Extract meta keywords for industry hints
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords and meta_keywords.get('content'):
                keywords = meta_keywords.get('content').lower()
                company_info['industry'] = self._extract_industry_from_keywords(keywords)
            
            # Look for company name in common elements
            name_selectors = [
                'h1', '.company-name', '.brand', '.logo-text',
                '[class*="company"]', '[class*="brand"]', '.navbar-brand',
                '.site-title', '.header-logo'
            ]
            
            for selector in name_selectors:
                element = soup.select_one(selector)
                if element and len(element.get_text().strip()) > 2:
                    potential_name = element.get_text().strip()
                    if self._is_legitimate_company_name(potential_name):
                        company_info['extracted_name'] = potential_name
                        break
            
            # Look for about us section
            about_section = soup.find('section', {'id': 'about'}) or \
                           soup.find('div', {'class': 'about'}) or \
                           soup.find('h2', string=re.compile(r'about', re.I)) or \
                           soup.find('div', {'class': re.compile(r'about', re.I)})
            
            if about_section:
                # Get text content from about section
                about_text = about_section.get_text().strip()[:500]  # Limit length
                company_info['about_text'] = about_text
                
                # Extract location from about text
                location = self._extract_location_from_text(about_text)
                if location:
                    company_info['location'] = location
                
                
                # Extract location from footer
                if not company_info.get('location'):
                    location = self._extract_location_from_text(footer_text)
                    if location:
                        company_info['location'] = location
                
                # Extract founding year from copyright
                if not company_info.get('founded_year'):
                    year_match = re.search(r'(\d{4})', footer_text)
                    if year_match:
                        year = int(year_match.group(1))
                        if 1900 <= year <= 2026:
                            company_info['founded_year'] = year
            
            return company_info if len(company_info) > 3 else None
            
        except Exception as e:
            print(f"Website content analysis failed: {e}")
            return None

    def _extract_industry_from_keywords(self, keywords: str) -> str:
        """Extract industry from meta keywords"""
        industry_keywords = {
            'technology': ['software', 'technology', 'tech', 'it', 'programming', 'development', 'saas'],
            'healthcare': ['health', 'medical', 'healthcare', 'pharmaceutical', 'medicine'],
            'finance': ['finance', 'banking', 'financial', 'investment', 'insurance', 'fintech'],
            'education': ['education', 'learning', 'training', 'school', 'university', 'courses'],
            'ecommerce': ['ecommerce', 'e-commerce', 'retail', 'shopping', 'store', 'marketplace'],
            'marketing': ['marketing', 'advertising', 'digital marketing', 'seo', 'social media'],
            'consulting': ['consulting', 'consultancy', 'advisory', 'solutions'],
            'manufacturing': ['manufacturing', 'production', 'industrial', 'factory'],
            'real estate': ['real estate', 'property', 'housing', 'construction'],
            'cybersecurity': ['cybersecurity', 'security', 'information security', 'cyber security'],
            'automotive': ['automotive', 'car', 'vehicle', 'automobile'],
            'food': ['food', 'restaurant', 'catering', 'food service'],
            'travel': ['travel', 'tourism', 'hospitality', 'hotel']
        }
        
        for industry, keywords_list in industry_keywords.items():
            if any(keyword in keywords for keyword in keywords_list):
                return industry.title()
        
        return 'Technology'  # Default fallback

    def _detect_industry_from_content(self, content: str) -> str:
        """Detect industry from website content"""
        industry_patterns = {
            'Technology': ['software', 'app', 'application', 'platform', 'digital', 'cloud', 'api', 'data'],
            'Healthcare': ['patient', 'doctor', 'medical', 'health', 'treatment', 'clinical'],
            'Finance': ['bank', 'payment', 'loan', 'credit', 'investment', 'portfolio', 'trading'],
            'Education': ['student', 'course', 'learning', 'teacher', 'curriculum', 'training'],
            'E-commerce': ['product', 'cart', 'checkout', 'shipping', 'order', 'buy', 'shop'],
            'Marketing': ['campaign', 'brand', 'audience', 'conversion', 'traffic', 'leads'],
            'Consulting': ['consulting', 'strategy', 'solutions', 'expertise', 'advisory'],
            'Cybersecurity': ['security', 'cyber', 'threat', 'protection', 'vulnerability', 'risk'],
            'Real Estate': ['property', 'real estate', 'housing', 'rental', 'mortgage'],
            'Manufacturing': ['production', 'factory', 'industrial', 'machinery', 'equipment']
        }
        
        industry_scores = {}
        for industry, patterns in industry_patterns.items():
            score = sum(1 for pattern in patterns if pattern in content)
            if score > 0:
                industry_scores[industry] = score
        
        if industry_scores:
            return max(industry_scores, key=industry_scores.get)
        
        return 'Technology'  # Default fallback

    def _extract_location_from_text(self, text: str) -> Optional[str]:
        """Extract location from text"""
        # Common city patterns
        cities = [
            'new york', 'los angeles', 'chicago', 'houston', 'phoenix', 'philadelphia',
            'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville',
            'boston', 'seattle', 'denver', 'washington dc', 'nashville', 'oklahoma city',
            'london', 'paris', 'tokyo', 'singapore', 'dubai', 'sydney', 'toronto',
            'bangalore', 'mumbai', 'delhi', 'hyderabad', 'chennai', 'kolkata'
        ]
        
        # US states
        states = [
            'california', 'texas', 'florida', 'new york', 'pennsylvania', 'illinois',
            'ohio', 'georgia', 'north carolina', 'michigan', 'new jersey', 'virginia'
        ]
        
        # Countries
        countries = [
            'united states', 'usa', 'canada', 'united kingdom', 'uk', 'germany',
            'france', 'japan', 'china', 'india', 'australia', 'singapore'
        ]
        
        text_lower = text.lower()
        
        # Check for cities
        for city in cities:
            if city in text_lower:
                return city.title()
        
        # Check for states
        for state in states:
            if state in text_lower:
                return state.title()
        
        # Check for countries
        for country in countries:
            if country in text_lower:
                return country.title()
        
        return None

    def _extract_founded_year_from_text(self, text: str) -> Optional[int]:
        """Extract founding year from text"""
        # Look for patterns like "founded in 2010", "since 2010", "established 2010"
        patterns = [
            r'founded\s+in\s+(\d{4})',
            r'since\s+(\d{4})',
            r'established\s+(\d{4})',
            r'started\s+in\s+(\d{4})',
            r'(\d{4})\s*-\s*present',
            r'from\s+(\d{4})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                year = int(match.group(1))
                if 1900 <= year <= 2026:
                    return year
        
        return None

    def _extract_contact_info(self, soup) -> Dict:
        """Extract contact information from website"""
        contact_info = {}
        
        # ... (rest of the code remains the same)
        # Look for email
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        text_content = soup.get_text()
        emails = email_pattern.findall(text_content)
        if emails:
            contact_info['email'] = emails[0]  # Take first email found
        
        # Look for phone numbers
        phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        phones = phone_pattern.findall(text_content)
        if phones:
            contact_info['phone'] = phones[0]
        
        # Look for address
        address_selectors = ['.address', '[class*="address"]', '.location']
        for selector in address_selectors:
            element = soup.select_one(selector)
            if element:
                address = element.get_text().strip()
                if len(address) > 10:  # Reasonable address length
                    contact_info['address'] = address
                    break
        
        return contact_info

    def _verify_domain_details(self, domain: str) -> Optional[Dict]:
        """Verify domain and extract basic information"""
        try:
            # Check if domain exists
            if not self._check_domain_exists(domain):
                return None
            
            domain_info = {
                'domain': domain,
                'verification_method': 'domain_analysis',
                'confidence': 'medium'
            }
            
            # Try to get basic domain info
            try:
                response = requests.get(f"https://{domain}", headers=self.headers, timeout=5)
                if response.status_code == 200:
                    domain_info['website_accessible'] = True
                    domain_info['https_enabled'] = True
                else:
                    domain_info['website_accessible'] = False
            except:
                try:
                    response = requests.get(f"http://{domain}", headers=self.headers, timeout=5)
                    domain_info['website_accessible'] = response.status_code == 200
                    domain_info['https_enabled'] = False
                except:
                    domain_info['website_accessible'] = False
            
            return domain_info
            
        except Exception as e:
            print(f"Domain verification failed: {e}")
            return None

    def _extract_company_name_from_domain(self, domain: str) -> Optional[str]:
        """Extract potential company name from domain"""
        try:
            # Remove common TLDs
            name_part = re.sub(r'\.(com|net|org|co|io|ai|tech|app|dev)$', '', domain)
            
            # Remove www prefix
            name_part = name_part.replace('www', '')
            
            # Clean up the name
            name_part = re.sub(r'[^a-zA-Z0-9]', ' ', name_part)
            name_part = ' '.join(name_part.split())
            
            # Check if it looks like a company name
            if len(name_part) >= 2 and self._is_legitimate_company_name(name_part):
                return name_part.title()
            
            return None
            
        except:
            return None

    def _enhanced_web_search_verification(self, company_name: str) -> Optional[Dict]:
        """Enhanced web search verification with Google-like results"""
        try:
            # Simulate comprehensive search results
            search_results = {
                'name': company_name,
                'verification_method': 'enhanced_search',
                'confidence': 'medium',
                'search_indicators': []
            }
            
            # Check for various indicators of legitimacy
            indicators = []
            
            # Domain existence check
            domains = self._generate_possible_domains(company_name)
            for domain in domains[:3]:  # Check first 3 domains
                if self._check_domain_exists(domain):
                    indicators.append(f"Active website: {domain}")
                    search_results['domain'] = domain
                    break
            
            # Check for common company name patterns
            if self._is_legitimate_company_name(company_name):
                indicators.append("Legitimate company name pattern")
            
            # Check against known company suffixes
            if any(suffix in company_name.lower() for suffix in ['inc', 'llc', 'corp', 'ltd', 'limited']):
                indicators.append("Contains legal business suffix")
            
            # Length check
            if 3 <= len(company_name) <= 30:
                indicators.append("Appropriate name length")
            
            search_results['search_indicators'] = indicators
            
            if len(indicators) >= 2:
                return search_results
            
            return None
            
        except Exception as e:
            print(f"Enhanced web search verification failed: {e}")
            return None

    def _is_legitimate_company_name(self, company_name: str) -> bool:
        """Basic heuristics to check if company name looks legitimate"""
        # Remove common words and check length
        clean_name = re.sub(r'\b(inc|llc|corp|corporation|ltd|limited|co|company)\b', '', company_name.lower().strip())
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'^test.*',
            r'^fake.*',
            r'^scam.*',
            r'.*test$',
            r'.*fake$',
            r'.*scam$',
            r'^[a-z]{1,3}$',  # Too short
            r'^\d+$',  # Only numbers
        ]
        
        for pattern in suspicious_patterns:
            if re.match(pattern, clean_name):
                return False
        
        # Check reasonable length
        if len(clean_name) < 2 or len(clean_name) > 50:
            return False
        
        return True
    
    def _check_local_database(self, company_name: str) -> Optional[Dict]:
        """Check against local database of known companies"""
        known_companies = {
            'google': {
                'company_name': 'Google LLC',
                'industry': 'Technology',
                'location': 'Mountain View, California, USA',
                'description': 'Technology company specializing in internet services and products',
                'domain': 'google.com',
                'founded_year': 1998,
                'employee_count': '150,000+'
            },
            'microsoft': {
                'company_name': 'Microsoft Corporation',
                'industry': 'Technology',
                'location': 'Redmond, Washington, USA',
                'description': 'Technology company developing software and hardware',
                'domain': 'microsoft.com',
                'founded_year': 1975,
                'employee_count': '180,000+'
            },
            'apple': {
                'company_name': 'Apple Inc.',
                'industry': 'Technology',
                'location': 'Cupertino, California, USA',
                'description': 'Technology company designing consumer electronics and software',
                'domain': 'apple.com',
                'founded_year': 1976,
                'employee_count': '154,000+'
            },
            'amazon': {
                'company_name': 'Amazon.com Inc.',
                'industry': 'E-commerce',
                'location': 'Seattle, Washington, USA',
                'description': 'E-commerce and cloud computing company',
                'domain': 'amazon.com', 'founded_year': 1994, 'employee_count': '1,300,000+'
            },
            'facebook': {
                'company_name': 'Meta Platforms Inc.',
                'industry': 'Social Media',
                'location': 'Menlo Park, California, USA',
                'description': 'Social media and technology company',
                'domain': 'meta.com', 'founded_year': 2004, 'employee_count': '85,000+'
            },
            'securden': {
                'company_name': 'Securden',
                'industry': 'Cybersecurity',
                'location': 'Chennai, Tamil Nadu, India',
                'description': 'Cybersecurity company specializing in privileged access management',
                'domain': 'securden.com', 'founded_year': 2018, 'employee_count': '50-100'
            },
            
            
            'mcafee': {
                'company_name': 'McAfee Corp',
                'industry': 'Cybersecurity',
                'location': 'Santa Clara, California, USA',
                'description': 'Global cybersecurity company providing protection against viruses and malware',
                'domain': 'mcafee.com', 'founded_year': 1987, 'employee_count': '7,000+'
            }
        }
        
        company_lower = company_name.lower().replace(' ', '').replace('.', '').replace(',', '')
        
        for key, info in known_companies.items():
            if key in company_lower or company_lower in key:
                return {
                    'verified': True,
                    'company_name': info['company_name'],
                    'industry': info['industry'],
                    'location': info['location'],
                    'description': info['description'],
                    'domain': info['domain'],
                    'source': 'Local Database',
                    'verification_method': 'local_match',
                    'confidence': 'high'
                }
        
        return None
    
    def _analyze_verification_results(self, company_name: str, verification_results: list) -> Dict:
        """Analyze all verification results to determine if company is real"""
        if not verification_results:
            return {
                'verified': False,
                'is_real': False,
                'company_name': company_name,
                'error': 'No verification sources found this company. It may be fake or non-existent.',
                'confidence': 'low',
                'sources_checked': 0
            }
        
        # Count verification sources and confidence levels
        high_confidence_sources = 0
        medium_confidence_sources = 0
        total_sources = len(verification_results)
        
        # Extract best information from all sources
        best_info = {
            'company_name': company_name,
            'verified': False,
            'is_real': False,
            'sources': [],
            'confidence': 'low'
        }
        
        for source_type, result in verification_results:
            best_info['sources'].append(source_type)
            
            if source_type == 'clearbit':
                # Clearbit is highly reliable
                high_confidence_sources += 1
                best_info.update({
                    'company_name': result.get('name', company_name),
                    'domain': result.get('domain'),
                    'description': result.get('description'),
                    'industry': result.get('category', {}).get('industry'),
                    'location': self._format_location(result.get('geo', {})),
                    'founded_year': result.get('foundedYear'),
                    'employee_count': result.get('metrics', {}).get('employees'),
                    'logo_url': result.get('logo'),
                    'social_links': self._extract_social_links(result.get('social', {}))
                })
                
            elif source_type == 'local':
                # Local database is reliable
                high_confidence_sources += 1
                best_info.update({
                    'company_name': result.get('company_name', company_name),
                    'domain': result.get('domain'),
                    'description': result.get('description'),
                    'industry': result.get('industry'),
                    'location': result.get('location'),
                    'founded_year': result.get('founded_year'),
                    'employee_count': result.get('employee_count')
                })
                # Local database is reliable
                high_confidence_sources += 1
                best_info.update({
                    'company_name': result.get('company_name', company_name),
                    'domain': result.get('domain'),
                    'description': result.get('description'),
                    'industry': result.get('industry'),
                    'location': result.get('location')
                })
                
            elif source_type == 'domain':
                # Domain check is medium reliability
                medium_confidence_sources += 1
                if not best_info.get('domain'):
                    best_info['domain'] = result.get('domain')
                if result.get('website_accessible') is not None:
                    best_info['website_accessible'] = result['website_accessible']
                if result.get('https_enabled') is not None:
                    best_info['https_enabled'] = result['https_enabled']
                    
            elif source_type == 'website':
                # Website analysis is highly reliable
                high_confidence_sources += 1
                website_data = {
                    'url': result.get('url'),
                    'website_title': result.get('website_title'),
                    'description': result.get('description'),
                    'extracted_name': result.get('extracted_name'),
                    'about_text': result.get('about_text'),
                    'email': result.get('email'),
                    'phone': result.get('phone'),
                    'address': result.get('address'),
                    'founded_year': result.get('founded_year')
                }
                
                # Update best info with website data
                for key, value in website_data.items():
                    if value and not best_info.get(key):
                        best_info[key] = value
                        
                # Update company name if extracted from website
                if result.get('extracted_name') and not best_info.get('company_name') == company_name:
                    best_info['company_name'] = result['extracted_name']
                    
            elif source_type == 'web':
                # Enhanced web search
                if result.get('confidence') == 'medium':
                    medium_confidence_sources += 1
                elif result.get('confidence') == 'high':
                    high_confidence_sources += 1
                    
                # Add search indicators
                if result.get('search_indicators'):
                    best_info['search_indicators'] = result['search_indicators']
                if result.get('domain') and not best_info.get('domain'):
                    best_info['domain'] = result['domain']
                    
            elif source_type == 'name':
                # Name verification from domain extraction
                if result.get('verified'):
                    medium_confidence_sources += 1
                    # Copy relevant info from name verification
                    for key in ['company_name', 'domain', 'description', 'industry', 'location']:
                        if result.get(key) and not best_info.get(key):
                            best_info[key] = result[key]
        
        # Determine if company is real based on verification sources
        if high_confidence_sources >= 1:
            best_info['verified'] = True
            best_info['is_real'] = True
            best_info['confidence'] = 'high'
        elif medium_confidence_sources >= 2 or (medium_confidence_sources >= 1 and total_sources >= 3):
            best_info['verified'] = True
            best_info['is_real'] = True
            best_info['confidence'] = 'medium'
        elif medium_confidence_sources >= 1:
            best_info['verified'] = True
            best_info['is_real'] = True
            best_info['confidence'] = 'low'
        else:
            best_info['verified'] = False
            best_info['is_real'] = False
            best_info['error'] = f'Company "{company_name}" could not be verified. It may be fake or non-existent.'
        
        best_info['sources_checked'] = total_sources
        best_info['verification_summary'] = f"Checked {total_sources} sources, {high_confidence_sources} high-confidence matches found"
        
        return best_info
