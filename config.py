# Database configuration (Wikimedia-style: adjust for your local/prod)
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'pass',  # Change this!
    'database': 'wikidb',  # Sample DB name
}

# Wikimedia-inspired thresholds
LAG_THRESHOLD_SEC = 5  # Alert if replica lag >5s
