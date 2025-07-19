import math
import statistics
import datetime
import re
import random
import string
from typing import List, Union, Dict, Any
import pytz
import urllib.parse


def calculator(expression: str) -> float:
    """Perform basic arithmetic calculations."""
    try:
        # Using eval for simple arithmetic expressions
        # Note: In production, use ast.literal_eval or a safer expression parser
        result = eval(expression)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}. Error: {str(e)}")


def compute_median(numbers: List[Union[int, float]]) -> float:
    """Compute the median of a list of numbers."""
    if not numbers:
        raise ValueError("List cannot be empty")
    return statistics.median(numbers)


def compute_std_dev(numbers: List[Union[int, float]]) -> float:
    """Compute the standard deviation of a list of numbers."""
    if len(numbers) < 2:
        raise ValueError("At least 2 numbers required for standard deviation")
    return statistics.stdev(numbers)


def compute_min_max(numbers: List[Union[int, float]]) -> Dict[str, Union[int, float]]:
    """Compute the minimum and maximum from a list of numbers."""
    if not numbers:
        raise ValueError("List cannot be empty")
    return {"min": min(numbers), "max": max(numbers)}


def calculate_combinations(n: int, r: int) -> int:
    """Calculate the number of possible combinations for given n and r."""
    if n < 0 or r < 0 or r > n:
        raise ValueError("Invalid parameters: n and r must be non-negative and r <= n")
    return math.comb(n, r)


def calculate_tax(income: float) -> Dict[str, float]:
    """Calculate US federal income tax based on income and 2025 tax brackets."""
    # 2025 tax brackets (simplified)
    brackets = [
        (0, 11600, 0.10),
        (11600, 47150, 0.12),
        (47150, 100525, 0.22),
        (100525, 191950, 0.24),
        (191950, 243725, 0.32),
        (243725, 609350, 0.35),
        (609350, float('inf'), 0.37)
    ]
    
    tax = 0
    for i, (lower, upper, rate) in enumerate(brackets):
        if income > lower:
            taxable_amount = min(income - lower, upper - lower)
            tax += taxable_amount * rate
    
    return {"tax_amount": tax, "effective_rate": (tax / income) * 100 if income > 0 else 0}


def add_days_to_date(date: str, days: int) -> str:
    """Add a number of days to a given date in YYYY-MM-DD format."""
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        new_date = date_obj + datetime.timedelta(days=days)
        return new_date.strftime("%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")


def get_weekday_from_date(date: str) -> str:
    """Get the weekday from a given date in YYYY-MM-DD format."""
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        return date_obj.strftime("%A")
    except ValueError as e:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")


def convert_time_zone(datetime_str: str, from_timezone: str, to_timezone: str) -> str:
    """Convert time between time zones."""
    try:
        # Parse the datetime string
        dt = datetime.datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        
        # Create timezone objects
        from_tz = pytz.timezone(from_timezone)
        to_tz = pytz.timezone(to_timezone)
        
        # Localize and convert
        if dt.tzinfo is None:
            dt = from_tz.localize(dt)
        
        converted_dt = dt.astimezone(to_tz)
        return converted_dt.isoformat()
    except Exception as e:
        raise ValueError(f"Error converting timezone: {str(e)}")


def calculate_date_diff(start_date: str, end_date: str) -> int:
    """Calculate the difference in days between two dates in YYYY-MM-DD format."""
    try:
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        return (end - start).days
    except ValueError as e:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")


def get_unix_timestamp(date: str) -> int:
    """Convert a date to a Unix timestamp."""
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        return int(date_obj.timestamp())
    except ValueError as e:
        raise ValueError(f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")


def get_current_datetime() -> str:
    """Get the current date and time."""
    # Return a fixed datetime for consistent results
    fixed_datetime = datetime.datetime(2024, 1, 15, 12, 30, 45)
    return fixed_datetime.isoformat()


def reverse_list(items: List[Any]) -> List[Any]:
    """Reverse the order of a list."""
    return items[::-1]


def deduplicate_list(items: List[Any]) -> List[Any]:
    """Remove duplicates from a list."""
    return list(dict.fromkeys(items))  # Preserves order


def sort_list(items: List[Any], descending: bool = False) -> List[Any]:
    """Sort a list in ascending or descending order."""
    sorted_items = sorted(items)
    return sorted_items[::-1] if descending else sorted_items


def filter_list(items: List[Any], condition: str) -> List[Any]:
    """Filter a list based on a condition."""
    try:
        # Create a safe filter function
        filter_func = lambda x: eval(condition, {"__builtins__": {"isinstance": isinstance, "int": int, "float": float, "str": str}}, {"x": x, "item": x, "value": x, "number": x, "string": x})
        return [item for item in items if filter_func(item)]
    except Exception as e:
        raise ValueError(f"Invalid filter condition: {condition}. Error: {str(e)}")


def word_count(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())


def char_count(text: str, character: str) -> int:
    """Count the number of specific characters in a text."""
    if len(character) != 1:
        raise ValueError("Character parameter must be a single character")
    return text.count(character)


def slugify_text(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from a text."""
    hashtags = re.findall(r'#\w+', text)
    return hashtags


def extract_urls(text: str) -> List[str]:
    """Extract URLs from a text."""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls


def validate_email(email: str) -> bool:
    """Validate the format of an email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def extract_phone_number(text: str) -> List[str]:
    """Extract phone numbers from text."""
    # Basic phone number pattern (US format)
    phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
    matches = re.findall(phone_pattern, text)
    return [''.join(match) for match in matches]


def convert_bases(number: str, from_base: int, to_base: int) -> str:
    """Convert a number from one base to another."""
    try:
        # Convert to decimal first
        decimal_num = int(number, from_base)
        
        # Convert to target base
        if to_base == 2:
            return bin(decimal_num)[2:]
        elif to_base == 8:
            return oct(decimal_num)[2:]
        elif to_base == 16:
            return hex(decimal_num)[2:].upper()
        elif to_base == 10:
            return str(decimal_num)
        else:
            # Custom base conversion
            if decimal_num == 0:
                return "0"
            
            digits = []
            while decimal_num:
                digits.append(str(decimal_num % to_base))
                decimal_num //= to_base
            
            return ''.join(digits[::-1])
    except ValueError as e:
        raise ValueError(f"Invalid number or base: {str(e)}")


def unit_conversion(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a value between different units.
    
    Available units for conversion:
    - Length: m (meters), ft (feet), km (kilometers), mi (miles)
    - Weight: kg (kilograms), lb (pounds)
    - Temperature: c (celsius), f (fahrenheit)
    
    Examples:
    - unit_conversion(1, 'm', 'ft') -> 3.28084
    - unit_conversion(32, 'f', 'c') -> 0.0
    - unit_conversion(2.2, 'lb', 'kg') -> 0.997903
    - unit_conversion(5, 'km', 'm') -> 5000.0
    - unit_conversion(1000, 'm', 'km') -> 1.0
    """
    # Simple conversion factors (you can expand this)
    conversions = {
        # Length
        ('m', 'ft'): 3.28084,
        ('ft', 'm'): 0.3048,
        ('km', 'mi'): 0.621371,
        ('mi', 'km'): 1.60934,
        ('km', 'm'): 1000.0,
        ('m', 'km'): 0.001,
        # Weight
        ('kg', 'lb'): 2.20462,
        ('lb', 'kg'): 0.453592,
        # Temperature
        ('c', 'f'): lambda c: c * 9/5 + 32,
        ('f', 'c'): lambda f: (f - 32) * 5/9,
    }
    
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        factor = conversions[key]
        if callable(factor):
            return factor(value)
        else:
            return value * factor
    else:
        raise ValueError(f"Unsupported conversion: {from_unit} to {to_unit}")


def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, float]:
    """Convert an amount between currencies.
    
    Available currencies for conversion:
    - USD (US Dollar)
    - EUR (Euro)
    - GBP (British Pound)
    - JPY (Japanese Yen)
    
    Examples:
    - convert_currency(100, 'USD', 'EUR') -> {'converted_amount': 85.0, 'rate': 0.85}
    - convert_currency(50, 'EUR', 'GBP') -> {'converted_amount': 43.0, 'rate': 0.86}
    """
    # Mock exchange rates (in production, use a real API)
    rates = {
        'USD': {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0},
        'EUR': {'USD': 1.18, 'GBP': 0.86, 'JPY': 129.4},
        'GBP': {'USD': 1.37, 'EUR': 1.16, 'JPY': 150.7},
        'JPY': {'USD': 0.009, 'EUR': 0.0077, 'GBP': 0.0066}
    }
    
    if from_currency == to_currency:
        return {"converted_amount": amount, "rate": 1.0}
    
    if from_currency in rates and to_currency in rates[from_currency]:
        rate = rates[from_currency][to_currency]
        converted = amount * rate
        return {"converted_amount": converted, "rate": rate}
    else:
        raise ValueError(f"Unsupported currency conversion: {from_currency} to {to_currency}")


def get_weather(city: str) -> Dict[str, Any]:
    """Get the current weather for a major city.
    
    Available cities (mock data):
    - new york: temperature 72°F, condition 'Partly Cloudy', humidity 65%
    - london: temperature 55°F, condition 'Rainy', humidity 80%
    - tokyo: temperature 68°F, condition 'Sunny', humidity 70%
    - paris: temperature 62°F, condition 'Cloudy', humidity 75%
    """
    # Mock weather data (in production, use a real weather API)
    weather_data = {
        'new york': {'temperature': 72, 'condition': 'Partly Cloudy', 'humidity': 65},
        'london': {'temperature': 55, 'condition': 'Rainy', 'humidity': 80},
        'tokyo': {'temperature': 68, 'condition': 'Sunny', 'humidity': 70},
        'paris': {'temperature': 62, 'condition': 'Cloudy', 'humidity': 75}
    }
    
    city_lower = city.lower()
    if city_lower in weather_data:
        return weather_data[city_lower]
    else:
        raise ValueError(f"Weather data not available for {city}")


def fetch_stock_price(symbol: str) -> Dict[str, Any]:
    """Fetch the current stock price for a symbol.
    
    Available symbols (mock data):
    - AAPL: price $150.25, change +$2.15, change_percent +1.45%
    - GOOGL: price $2750.80, change -$15.20, change_percent -0.55%
    - MSFT: price $310.45, change +$5.30, change_percent +1.74%
    - TSLA: price $850.75, change +$25.50, change_percent +3.09%
    """
    # Mock stock data (in production, use a real stock API)
    stock_data = {
        'AAPL': {'price': 150.25, 'change': 2.15, 'change_percent': 1.45},
        'GOOGL': {'price': 2750.80, 'change': -15.20, 'change_percent': -0.55},
        'MSFT': {'price': 310.45, 'change': 5.30, 'change_percent': 1.74},
        'TSLA': {'price': 850.75, 'change': 25.50, 'change_percent': 3.09}
    }
    
    if symbol.upper() in stock_data:
        return stock_data[symbol.upper()]
    else:
        raise ValueError(f"Stock data not available for {symbol}")


def fetch_crypto_price(symbol: str) -> Dict[str, Any]:
    """Fetch the current price of a cryptocurrency.
    
    Available symbols (mock data):
    - BTC: price $45,000.00, change_24h +$1,200.50, change_percent +2.74%
    - ETH: price $3,200.75, change_24h -$45.25, change_percent -1.39%
    - ADA: price $1.25, change_24h +$0.05, change_percent +4.17%
    - DOT: price $25.80, change_24h +$1.20, change_percent +4.88%
    """
    # Mock crypto data (in production, use a real crypto API)
    crypto_data = {
        'BTC': {'price': 45000.00, 'change_24h': 1200.50, 'change_percent': 2.74},
        'ETH': {'price': 3200.75, 'change_24h': -45.25, 'change_percent': -1.39},
        'ADA': {'price': 1.25, 'change_24h': 0.05, 'change_percent': 4.17},
        'DOT': {'price': 25.80, 'change_24h': 1.20, 'change_percent': 4.88}
    }
    
    if symbol.upper() in crypto_data:
        return crypto_data[symbol.upper()]
    else:
        raise ValueError(f"Crypto data not available for {symbol}")


def send_email(to: str, subject: str, body: str) -> Dict[str, str]:
    """Send an email to a recipient."""
    # Mock email sending (in production, use a real email service)
    return {
        "status": "sent",
        "message_id": f"msg_{random.randint(100000, 999999)}",
        "to": to,
        "subject": subject
    }


def send_slack_message(channel: str, message: str) -> Dict[str, str]:
    """Send a message to a Slack channel."""
    # Mock Slack message (in production, use Slack API)
    return {
        "status": "sent",
        "channel": channel,
        "timestamp": datetime.datetime.now().isoformat()
    }


def post_to_x(message: str) -> Dict[str, str]:
    """Post a message to X (Twitter)."""
    # Mock X posting (in production, use X API)
    return {
        "status": "posted",
        "tweet_id": f"tweet_{random.randint(1000000000000000000, 9999999999999999999)}",
        "message": message[:280]  # X character limit
    }


def create_event(title: str, datetime_str: str, location: str) -> Dict[str, str]:
    """Create a calendar event."""
    # Mock calendar event creation (in production, use calendar API)
    return {
        "status": "created",
        "event_id": f"event_{random.randint(100000, 999999)}",
        "title": title,
        "datetime": datetime_str,
        "location": location
    }


def set_reminder(message: str, datetime_str: str) -> Dict[str, str]:
    """Set a reminder for a task."""
    # Mock reminder setting (in production, use reminder service)
    return {
        "status": "set",
        "reminder_id": f"reminder_{random.randint(100000, 999999)}",
        "message": message,
        "datetime": datetime_str
    }


def add_to_todo_list(task: str) -> Dict[str, str]:
    """Add a task to the to-do list."""
    # Mock todo list addition (in production, use todo service)
    return {
        "status": "added",
        "task_id": f"task_{random.randint(100000, 999999)}",
        "task": task
    }


def web_search(query: str) -> List[Dict[str, str]]:
    """Perform a web search for news in major cities.
    
    Supported cities: new york, london, tokyo, paris
    Query format: "news in [city]" or "[city] news"
    """
    query_lower = query.lower()
    
    # Fixed news results for each city
    city_news = {
        'new york': [
            {
                "title": "Breaking: Major Infrastructure Project Announced in New York",
                "url": "https://nytimes.com/breaking-news/major-infrastructure-project",
                "snippet": "Latest breaking news from New York. Officials have announced plans for a $2.3 billion infrastructure project that will significantly impact the city's future development and create thousands of jobs."
            },
            {
                "title": "New York Business & Economy: Tech Startup Raises $50M in Funding",
                "url": "https://nypost.com/business/tech-startup-raises-50m-funding",
                "snippet": "Business news from New York. A local technology startup has secured $50 million in Series B funding, with plans to create hundreds of new jobs in the Manhattan area."
            },
            {
                "title": "What's happening in New York: New Cultural Festival Coming This Summer",
                "url": "https://amny.com/local/new-cultural-festival-coming-summer",
                "snippet": "Local news update from New York. The city will host a major cultural festival this summer, promising to bring thousands of visitors and boost local tourism in all five boroughs."
            },
            {
                "title": "New York Transportation: Subway Improvements Planned for 2024",
                "url": "https://nytimes.com/transportation/subway-improvements-2024",
                "snippet": "Transportation news from New York. The MTA has announced comprehensive subway improvements planned for 2024, including new trains and station upgrades across the network."
            }
        ],
        'london': [
            {
                "title": "Breaking: London Announces New Green Energy Initiative",
                "url": "https://bbc.com/breaking-news/london-green-energy-initiative",
                "snippet": "Latest breaking news from London. The Mayor has announced a major green energy initiative that will make London one of the most sustainable cities in Europe by 2030."
            },
            {
                "title": "London Business: Financial District Sees Record Growth",
                "url": "https://theguardian.com/business/financial-district-record-growth",
                "snippet": "Business news from London. The City of London financial district has reported record growth in fintech investments, with over £2 billion in new funding this quarter."
            },
            {
                "title": "What's happening in London: New Museum Opening in South Bank",
                "url": "https://telegraph.co.uk/local/new-museum-south-bank",
                "snippet": "Local news update from London. A new contemporary art museum is set to open on the South Bank, featuring works from emerging British artists and international collections."
            },
            {
                "title": "London Culture: West End Theaters Announce New Season",
                "url": "https://standard.co.uk/culture/west-end-new-season-announcement",
                "snippet": "Culture news from London. West End theaters have announced their new season lineup, featuring world premieres and revivals of classic productions."
            }
        ],
        'tokyo': [
            {
                "title": "Breaking: Tokyo Unveils Advanced AI Transportation System",
                "url": "https://japantimes.co.jp/breaking-news/tokyo-ai-transportation-system",
                "snippet": "Latest breaking news from Tokyo. The city has unveiled an advanced AI-powered transportation system that will revolutionize public transit and reduce congestion by 30%."
            },
            {
                "title": "Tokyo Technology: Robot Restaurant Chain Expands Nationwide",
                "url": "https://asahi.com/technology/robot-restaurant-chain-expansion",
                "snippet": "Technology news from Tokyo. A popular robot restaurant chain is expanding nationwide, with plans to open 50 new locations across Japan, creating innovative dining experiences."
            },
            {
                "title": "What's happening in Tokyo: Cherry Blossom Festival Dates Announced",
                "url": "https://mainichi.jp/local/cherry-blossom-festival-dates",
                "snippet": "Local news update from Tokyo. The annual cherry blossom festival dates have been announced, with peak viewing expected in late March and early April across the city."
            },
            {
                "title": "Tokyo Business: Gaming Industry Reports Record Profits",
                "url": "https://yomiuri.co.jp/business/gaming-industry-record-profits",
                "snippet": "Business news from Tokyo. Japan's gaming industry has reported record profits, with Tokyo-based companies leading global innovation in mobile and console gaming."
            }
        ],
        'paris': [
            {
                "title": "Breaking: Paris Announces Major Cultural Heritage Restoration",
                "url": "https://lemonde.fr/breaking-news/paris-cultural-heritage-restoration",
                "snippet": "Latest breaking news from Paris. The city has announced a major restoration project for historic monuments, including the Notre-Dame Cathedral and several iconic bridges."
            },
            {
                "title": "Paris Fashion: Haute Couture Week Sets New Attendance Records",
                "url": "https://lefigaro.fr/fashion/haute-couture-week-attendance-records",
                "snippet": "Fashion news from Paris. Paris Fashion Week has set new attendance records, with over 100,000 visitors and buyers from around the world attending the prestigious event."
            },
            {
                "title": "What's happening in Paris: New Art District Opens in Marais",
                "url": "https://liberation.fr/local/new-art-district-marais",
                "snippet": "Local news update from Paris. A new contemporary art district has opened in the Marais neighborhood, featuring galleries, studios, and cultural spaces for emerging artists."
            },
            {
                "title": "Paris Transportation: Metro System Gets Major Upgrade",
                "url": "https://leparisien.fr/transportation/metro-system-major-upgrade",
                "snippet": "Transportation news from Paris. The Paris Metro system is receiving a major upgrade with new trains, improved accessibility, and extended service hours across all lines."
            }
        ]
    }
    
    # Extract city from query
    detected_city = None
    for city in city_news:
        if city in query_lower or city.replace(' ', '') in query_lower.replace(' ', ''):
            detected_city = city
            break
    
    if not detected_city:
        return [
            {
                "title": f"Search results for: {query}",
                "url": f"https://search.example.com?q={urllib.parse.quote(query)}",
                "snippet": f"General search results for '{query}'. Try searching for news in New York, London, Tokyo, or Paris for city-specific news."
            }
        ]
    
    return city_news[detected_city]


def notion_search(query: str) -> List[Dict[str, str]]:
    """Search for pages in a Notion workspace."""
    # Mock Notion search results (in production, use Notion API)
    query_lower = query.lower()
    
    # Predefined mock Notion pages for different query types
    notion_pages = {
        'project': [
            {
                "title": "Q1 Project Planning",
                "url": "https://notion.so/project-planning-2024",
                "snippet": "Comprehensive project planning document for Q1 2024. Includes timelines, milestones, and resource allocation for all major initiatives."
            },
            {
                "title": "Product Roadmap 2024",
                "url": "https://notion.so/product-roadmap-2024",
                "snippet": "Detailed product roadmap outlining feature releases, development phases, and strategic goals for the upcoming year."
            },
            {
                "title": "Team Meeting Notes - Project Updates",
                "url": "https://notion.so/team-meeting-notes",
                "snippet": "Weekly team meeting notes covering project updates, blockers, and action items from the development team."
            }
        ],
        'meeting': [
            {
                "title": "Weekly Standup Notes",
                "url": "https://notion.so/weekly-standup",
                "snippet": "Daily standup meeting notes with team updates, progress tracking, and action items for the development team."
            },
            {
                "title": "Board Meeting - March 2024",
                "url": "https://notion.so/board-meeting-march",
                "snippet": "Board meeting agenda and minutes covering strategic decisions, financial updates, and company direction."
            },
            {
                "title": "Client Meeting - Project Review",
                "url": "https://notion.so/client-meeting-review",
                "snippet": "Client meeting notes and project review discussion points, including feedback and next steps."
            }
        ],
        'budget': [
            {
                "title": "Annual Budget 2024",
                "url": "https://notion.so/annual-budget-2024",
                "snippet": "Comprehensive annual budget breakdown including department allocations, projected expenses, and revenue forecasts."
            },
            {
                "title": "Marketing Budget Tracker",
                "url": "https://notion.so/marketing-budget",
                "snippet": "Real-time marketing budget tracker with campaign spending, ROI metrics, and budget allocation across channels."
            },
            {
                "title": "Expense Reports Q1",
                "url": "https://notion.so/expense-reports-q1",
                "snippet": "Quarterly expense reports with detailed breakdowns, approval workflows, and reimbursement tracking."
            }
        ],
        'research': [
            {
                "title": "Market Research - Competitor Analysis",
                "url": "https://notion.so/market-research",
                "snippet": "Comprehensive market research document analyzing competitors, market trends, and opportunities in our industry."
            },
            {
                "title": "User Research Findings",
                "url": "https://notion.so/user-research",
                "snippet": "User research insights and findings from interviews, surveys, and usability testing sessions."
            },
            {
                "title": "Technology Research - AI Integration",
                "url": "https://notion.so/tech-research-ai",
                "snippet": "Research document on AI integration opportunities, vendor evaluations, and implementation strategies."
            }
        ]
    }
    
    # Find matching pages based on query keywords
    matching_pages = []
    for category, pages in notion_pages.items():
        if category in query_lower:
            matching_pages.extend(pages)
    
    # If no specific category matches, return general results
    if not matching_pages:
        matching_pages = [
            {
                "title": f"Search Results for: {query}",
                "url": f"https://notion.so/search?q={urllib.parse.quote(query)}",
                "snippet": f"General search results for '{query}' in your Notion workspace. Try searching for 'project', 'meeting', 'budget', or 'research' for more specific results."
            }
        ]
    
    return matching_pages[:3]  # Return top 3 results


def retrieve_data(query: str) -> List[Dict[str, str]]:
    """Retrieve information from a local knowledge base.
    
    Supports searching through:
    - Support documentation
    - Standard Operating Procedures (SOPs)
    - Onboarding documents
    - Company policies
    - Technical guides
    
    """
    query_lower = query.lower()
    
    # Comprehensive mock knowledge base
    knowledge_base = {
        # Support Documentation
        'support': [
            {
                "title": "Password Reset Procedure",
                "content": "To reset your password: 1) Go to login page, 2) Click 'Forgot Password', 3) Enter your email, 4) Check email for reset link, 5) Create new password with 8+ characters including uppercase, lowercase, number, and symbol. Contact IT support if issues persist.",
                "source": "IT Support Documentation",
                "category": "support",
                "tags": ["password", "reset", "login", "security"]
            },
            {
                "title": "VPN Connection Guide",
                "content": "VPN setup: 1) Download VPN client from company portal, 2) Install and launch application, 3) Enter your company credentials, 4) Select nearest server location, 5) Click connect. For troubleshooting, check firewall settings and contact IT support.",
                "source": "IT Support Documentation",
                "category": "support",
                "tags": ["vpn", "remote", "network", "security"]
            },
            {
                "title": "Email Configuration",
                "content": "Email setup instructions: 1) Open email client, 2) Add new account, 3) Enter email: username@company.com, 4) Password: your company password, 5) Server settings: IMAP for incoming (port 993), SMTP for outgoing (port 587), 6) Enable SSL/TLS encryption.",
                "source": "IT Support Documentation",
                "category": "support",
                "tags": ["email", "configuration", "imap", "smtp"]
            },
            {
                "title": "Software Installation Guide",
                "content": "Standard software installation: 1) Download from approved software portal, 2) Run installer as administrator, 3) Accept license agreement, 4) Choose installation directory, 5) Complete installation, 6) Restart computer if prompted. Contact IT for licensed software.",
                "source": "IT Support Documentation",
                "category": "support",
                "tags": ["software", "installation", "admin", "portal"]
            }
        ],
        
        # Standard Operating Procedures (SOPs)
        'sop': [
            {
                "title": "Customer Service Call Handling SOP",
                "content": "Customer call procedure: 1) Answer within 3 rings, 2) Greet with company name and your name, 3) Listen actively and take notes, 4) Confirm understanding, 5) Provide solution or escalate if needed, 6) Follow up within 24 hours, 7) Document in CRM system. Always maintain professional tone.",
                "source": "Operations Manual",
                "category": "sop",
                "tags": ["customer", "service", "calls", "procedure"]
            },
            {
                "title": "Data Backup Procedure",
                "content": "Daily backup process: 1) Verify backup software is running, 2) Check backup logs for errors, 3) Test restore from previous backup, 4) Update backup schedule if needed, 5) Document any issues. Weekly: Full system backup. Monthly: Offsite backup verification.",
                "source": "IT Operations Manual",
                "category": "sop",
                "tags": ["backup", "data", "security", "disaster recovery"]
            },
            {
                "title": "Incident Response Protocol",
                "content": "Security incident response: 1) Immediately report to security team, 2) Isolate affected systems, 3) Preserve evidence, 4) Assess impact and scope, 5) Implement containment measures, 6) Notify stakeholders, 7) Document incident details, 8) Conduct post-incident review.",
                "source": "Security Operations Manual",
                "category": "sop",
                "tags": ["incident", "security", "response", "protocol"]
            },
            {
                "title": "Quality Assurance Testing SOP",
                "content": "QA testing process: 1) Review requirements and test cases, 2) Set up test environment, 3) Execute test cases systematically, 4) Document defects with screenshots, 5) Verify fixes in next build, 6) Sign off on release readiness, 7) Update test documentation.",
                "source": "Quality Assurance Manual",
                "category": "sop",
                "tags": ["qa", "testing", "quality", "defects"]
            }
        ],
        
        # Onboarding Documents
        'onboarding': [
            {
                "title": "New Employee Onboarding Checklist",
                "content": "First day: 1) Complete HR paperwork, 2) Get company ID and access cards, 3) Set up computer and email, 4) Meet with manager and team, 5) Review company policies. Week 1: Complete training modules, set up benefits, attend orientation. Month 1: Performance review meeting, goal setting.",
                "source": "Human Resources",
                "category": "onboarding",
                "tags": ["employee", "onboarding", "checklist", "hr"]
            },
            {
                "title": "Company Culture and Values",
                "content": "Our values: Integrity, Innovation, Collaboration, Customer Focus. Culture: Open communication, continuous learning, work-life balance, diversity and inclusion. We encourage feedback, celebrate achievements, and support professional development. Regular team events and recognition programs.",
                "source": "Human Resources",
                "category": "onboarding",
                "tags": ["culture", "values", "company", "culture"]
            },
            {
                "title": "Benefits and Compensation Guide",
                "content": "Benefits include: Health, dental, vision insurance (80% employer paid), 401(k) with 4% match, 15 days PTO, 10 holidays, flexible work arrangements, professional development budget, wellness programs. Compensation reviews annually. Performance bonuses based on company and individual goals.",
                "source": "Human Resources",
                "category": "onboarding",
                "tags": ["benefits", "compensation", "insurance", "pto"]
            },
            {
                "title": "Technology Setup Guide",
                "content": "Equipment provided: Laptop, monitor, keyboard, mouse, headset, company phone. Software: Office 365, Slack, Zoom, project management tools, VPN client. Access to: Company intranet, shared drives, CRM system, time tracking. IT support available 8am-6pm EST.",
                "source": "IT Department",
                "category": "onboarding",
                "tags": ["technology", "equipment", "software", "access"]
            }
        ],
        
        # Company Policies
        'policies': [
            {
                "title": "Expense Reimbursement Policy",
                "content": "Expense submission: Submit within 30 days, include receipts, use company expense form. Approved expenses: Travel, meals (up to $50/day), office supplies, professional development. Not covered: Personal expenses, alcohol, entertainment. Approval required for expenses over $500.",
                "source": "Finance Department",
                "category": "policies",
                "tags": ["expense", "reimbursement", "policy", "finance"]
            },
            {
                "title": "Remote Work Policy",
                "content": "Remote work available: Up to 3 days per week, manager approval required. Requirements: Dedicated workspace, reliable internet, video camera for meetings, core hours 10am-4pm EST. Equipment provided by company. Security: Use VPN, secure home network, no public WiFi for work.",
                "source": "Human Resources",
                "category": "policies",
                "tags": ["remote", "work", "policy", "flexible"]
            },
            {
                "title": "Social Media Policy",
                "content": "Guidelines: Be professional, respect confidentiality, don't share company secrets, use disclaimers for personal opinions. Prohibited: Sharing confidential information, negative comments about company, inappropriate content. Company accounts managed by marketing team only.",
                "source": "Marketing Department",
                "category": "policies",
                "tags": ["social media", "policy", "confidentiality", "professional"]
            },
            {
                "title": "Dress Code Policy",
                "content": "Business casual: Collared shirts, slacks, skirts, dresses, closed-toe shoes. Avoid: Jeans, t-shirts, flip-flops, revealing clothing. Client meetings: Business professional attire required. Casual Fridays: Jeans allowed with company logo or solid colors.",
                "source": "Human Resources",
                "category": "policies",
                "tags": ["dress code", "attire", "professional", "casual"]
            }
        ],
        
        # Technical Documentation
        'technical': [
            {
                "title": "API Documentation",
                "content": "REST API endpoints: GET /api/users, POST /api/users, PUT /api/users/{id}, DELETE /api/users/{id}. Authentication: Bearer token required. Rate limits: 1000 requests/hour. Response format: JSON. Error codes: 400 (bad request), 401 (unauthorized), 404 (not found), 500 (server error).",
                "source": "Engineering Team",
                "category": "technical",
                "tags": ["api", "documentation", "endpoints", "authentication"]
            },
            {
                "title": "Database Schema Guide",
                "content": "Main tables: users (id, email, name, role), products (id, name, price, category), orders (id, user_id, product_id, quantity, date), customers (id, name, email, phone). Relationships: Foreign keys between tables. Indexes on frequently queried columns. Backup daily at 2am.",
                "source": "Engineering Team",
                "category": "technical",
                "tags": ["database", "schema", "tables", "relationships"]
            },
            {
                "title": "Deployment Process",
                "content": "Deployment steps: 1) Code review and approval, 2) Run automated tests, 3) Create deployment branch, 4) Deploy to staging environment, 5) Run integration tests, 6) Deploy to production, 7) Monitor for 30 minutes, 8) Update documentation. Rollback plan available.",
                "source": "DevOps Team",
                "category": "technical",
                "tags": ["deployment", "process", "staging", "production"]
            },
            {
                "title": "Security Best Practices",
                "content": "Password requirements: 12+ characters, uppercase, lowercase, numbers, symbols. Multi-factor authentication required. Regular security updates. No sharing credentials. Report suspicious activity immediately. Use company-approved software only. Encrypt sensitive data.",
                "source": "Security Team",
                "category": "technical",
                "tags": ["security", "passwords", "authentication", "encryption"]
            }
        ]
    }
    
    # Search logic - find matching documents based on query keywords
    matching_docs = []
    query_words = query_lower.split()
    
    # Search through all categories
    for category, documents in knowledge_base.items():
        for doc in documents:
            # Check if any query word matches title, content, or tags
            doc_text = f"{doc['title']} {doc['content']} {' '.join(doc['tags'])}".lower()
            
            # Calculate relevance score based on word matches
            relevance_score = 0
            for word in query_words:
                if word in doc_text:
                    relevance_score += 1
                    # Bonus for exact matches in title
                    if word in doc['title'].lower():
                        relevance_score += 2
                    # Bonus for tag matches
                    if word in doc['tags']:
                        relevance_score += 1
            
            if relevance_score > 0:
                matching_docs.append((doc, relevance_score))
    
    # Sort by relevance score (highest first) and return top results
    matching_docs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 3 most relevant documents
    results = []
    for doc, score in matching_docs[:3]:
        results.append({
            "title": doc["title"],
            "content": doc["content"],
            "source": doc["source"],
            "category": doc["category"],
            "relevance_score": score
        })
    
    # If no matches found, return a helpful message
    if not results:
        results = [{
            "title": f"No results found for: {query}",
            "content": f"Try searching for: support, sop, onboarding, policies, technical, password, email, vpn, backup, incident, qa, employee, benefits, expense, remote, api, database, deployment, security",
            "source": "Knowledge Base Search",
            "category": "search_help",
            "relevance_score": 0
        }]
    
    return results


def query_database(query: str, dataset: str) -> List[Dict[str, Any]]:
    """Run a SQL query on customer, sales, or inventory tables.
    
    Valid datasets: 'customers', 'sales', 'inventory'
    Supported SQL operations: SELECT, WHERE, ORDER BY, LIMIT, COUNT, SUM, AVG, MAX, MIN
    """
    import sqlite3
    
    # Validate dataset
    valid_datasets = ['customers', 'sales', 'inventory']
    if dataset not in valid_datasets:
        raise ValueError(f"Invalid dataset. Must be one of: {valid_datasets}")
    
    # Basic SQL validation - check for dangerous operations
    query_upper = query.upper().strip()
    
    # Block dangerous operations
    dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'TRUNCATE', 'EXEC', 'EXECUTE']
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            raise ValueError(f"Operation '{keyword}' is not allowed for security reasons")
    
    # Validate it's a SELECT query
    if not query_upper.startswith('SELECT'):
        raise ValueError("Only SELECT queries are allowed")
    
    # Create toy database with sample data
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create toy tables with realistic data
    if dataset == 'customers':
        cursor.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                city TEXT,
                country TEXT,
                join_date TEXT,
                total_spent REAL,
                status TEXT
            )
        ''')
        
        # Insert sample customer data
        customers_data = [
            (1, 'John Smith', 'john@email.com', 'New York', 'USA', '2023-01-15', 1250.50, 'active'),
            (2, 'Maria Garcia', 'maria@email.com', 'Los Angeles', 'USA', '2023-02-20', 890.25, 'active'),
            (3, 'David Johnson', 'david@email.com', 'Chicago', 'USA', '2023-03-10', 2100.75, 'active'),
            (4, 'Sarah Wilson', 'sarah@email.com', 'Houston', 'USA', '2023-01-05', 750.00, 'inactive'),
            (5, 'Michael Brown', 'michael@email.com', 'Phoenix', 'USA', '2023-04-12', 1650.30, 'active'),
            (6, 'Emma Davis', 'emma@email.com', 'Philadelphia', 'USA', '2023-02-28', 980.45, 'active'),
            (7, 'James Miller', 'james@email.com', 'San Antonio', 'USA', '2023-03-22', 1120.80, 'active'),
            (8, 'Lisa Anderson', 'lisa@email.com', 'San Diego', 'USA', '2023-01-30', 1450.90, 'inactive'),
            (9, 'Robert Taylor', 'robert@email.com', 'Dallas', 'USA', '2023-04-05', 890.60, 'active'),
            (10, 'Jennifer Martinez', 'jennifer@email.com', 'San Jose', 'USA', '2023-02-15', 1780.25, 'active')
        ]
        cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)', customers_data)
        
    elif dataset == 'sales':
        cursor.execute('''
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_name TEXT,
                quantity INTEGER,
                unit_price REAL,
                total_amount REAL,
                sale_date TEXT,
                region TEXT
            )
        ''')
        
        # Insert sample sales data
        sales_data = [
            (1, 1, 'Laptop', 1, 1200.00, 1200.00, '2024-01-15', 'East'),
            (2, 2, 'Mouse', 3, 25.00, 75.00, '2024-01-16', 'West'),
            (3, 3, 'Keyboard', 2, 80.00, 160.00, '2024-01-17', 'Central'),
            (4, 1, 'Monitor', 1, 300.00, 300.00, '2024-01-18', 'East'),
            (5, 4, 'Headphones', 1, 150.00, 150.00, '2024-01-19', 'South'),
            (6, 5, 'Tablet', 1, 500.00, 500.00, '2024-01-20', 'West'),
            (7, 2, 'Webcam', 1, 100.00, 100.00, '2024-01-21', 'West'),
            (8, 6, 'Printer', 1, 200.00, 200.00, '2024-01-22', 'East'),
            (9, 7, 'Speakers', 2, 75.00, 150.00, '2024-01-23', 'Central'),
            (10, 8, 'Microphone', 1, 120.00, 120.00, '2024-01-24', 'West')
        ]
        cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?)', sales_data)
        
    elif dataset == 'inventory':
        cursor.execute('''
            CREATE TABLE inventory (
                id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                quantity_in_stock INTEGER,
                unit_price REAL,
                supplier TEXT,
                last_restocked TEXT,
                reorder_level INTEGER
            )
        ''')
        
        # Insert sample inventory data
        inventory_data = [
            (1, 'Laptop', 'Electronics', 25, 1200.00, 'TechCorp', '2024-01-10', 10),
            (2, 'Mouse', 'Accessories', 150, 25.00, 'AccessoryPro', '2024-01-12', 50),
            (3, 'Keyboard', 'Accessories', 75, 80.00, 'AccessoryPro', '2024-01-08', 30),
            (4, 'Monitor', 'Electronics', 40, 300.00, 'TechCorp', '2024-01-15', 15),
            (5, 'Headphones', 'Audio', 60, 150.00, 'AudioMax', '2024-01-11', 25),
            (6, 'Tablet', 'Electronics', 30, 500.00, 'TechCorp', '2024-01-09', 12),
            (7, 'Webcam', 'Accessories', 45, 100.00, 'AccessoryPro', '2024-01-13', 20),
            (8, 'Printer', 'Electronics', 20, 200.00, 'PrintTech', '2024-01-14', 8),
            (9, 'Speakers', 'Audio', 35, 75.00, 'AudioMax', '2024-01-07', 15),
            (10, 'Microphone', 'Audio', 25, 120.00, 'AudioMax', '2024-01-16', 10)
        ]
        cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?, ?, ?)', inventory_data)
    
    try:
        # Execute the query
        cursor.execute(query)
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Fetch results
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        return [
            {
                "query": query,
                "dataset": dataset,
                "results": results,
                "row_count": len(results),
                "columns": columns
            }
        ]
        
    except sqlite3.Error as e:
        raise ValueError(f"SQL Error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Query execution error: {str(e)}")
    finally:
        conn.close()


def generate_password(length: int, use_symbols: bool = True, use_numbers: bool = True, use_uppercase: bool = True) -> str:
    """Generate a random password."""
    if length < 1:
        raise ValueError("Password length must be at least 1")
    
    chars = string.ascii_lowercase
    
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not chars:
        raise ValueError("At least one character type must be enabled")
    
    return ''.join(random.choice(chars) for _ in range(length))
