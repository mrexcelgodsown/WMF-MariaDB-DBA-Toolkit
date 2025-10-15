import os

# Define project structure and file contents
files = {
    'README.md': '''# WMF MariaDB DBA Toolkit

A Python-based toolkit for MariaDB administration, inspired by the Wikimedia Foundation's production database needs for Wikipedia and sister projects. Demonstrates skills in replication management, query optimization, and automation at scale.

## Why Wikimedia-Focused?
- Wikimedia uses MariaDB for high-availability, read-heavy workloads (~50k QPS peak on English Wikipedia).
- Tools here address replication topologies (multi-shard, semi-sync), schema design (e.g., unsigned ints, VARBINARY), and lag handling (<5s threshold).
- Potential for upstream contributions to MediaWiki or MariaDB projects.

## Quick Start
1. `pip install -r requirements.txt`
2. Edit `config.py` with DB details.
3. Run: `python scripts/replication_monitor.py`

## Tools
- **replication_monitor.py**: Checks lag, prints topology graph, alerts on issues.
- **schema_optimizer.py**: Suggests indexes/queries for MediaWiki tables (e.g., page_touched caching).
- **backup_validator.py**: Validates backups via checksums.

## Testing
`python -m pytest tests/`

License: MIT (open-source friendly for Wikimedia contribs).
''',
    'config.py': '''# Database configuration (Wikimedia-style: adjust for your local/prod)
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'pass',  # Change this!
    'database': 'wikidb',  # Sample DB name
}

# Wikimedia-inspired thresholds
LAG_THRESHOLD_SEC = 5  # Alert if replica lag >5s
''',
    'requirements.txt': '''pymysql==1.1.0
''',
    'scripts/replication_monitor.py': '''#!/usr/bin/env python3
"""
MariaDB Replication Monitor - Inspired by Wikimedia's production setup.
Monitors lag, prints simple topology graph, and simulates alerting.
Handles multi-site topologies (e.g., primary -> replicas across shards).
"""

import pymysql
from config import DB_CONFIG, LAG_THRESHOLD_SEC

def connect_db():
    """Connect to MariaDB (primary or replica)."""
    return pymysql.connect(**DB_CONFIG)

def get_replication_lag(db):
    """Fetch replication lag in seconds (SHOW SLAVE STATUS)."""
    with db.cursor() as cursor:
        cursor.execute("SHOW SLAVE STATUS;")
        result = cursor.fetchone()
        if result:
            lag = int(result[32]) if result[32] else 0  # Seconds_Behind_Master
            return lag
        return 0

def get_topology(db):
    """Simple topology: primary/replicas (extend for full Orchestrator-like graph)."""
    with db.cursor() as cursor:
        # Assume a 'topology' table or query SHOW SLAVE HOSTS
        cursor.execute("SHOW SLAVE HOSTS;")
        hosts = [row[0] for row in cursor.fetchall()]
        return {'primary': DB_CONFIG['host'], 'replicas': hosts}

def print_topology_graph(topology):
    """Text-based graph (e.g., for ASCII viz; extend to Graphviz)."""
    print("Replication Topology:")
    print(f"Primary: {topology['primary']}")
    for replica in topology['replicas']:
        print(f"  └─ Replica: {replica}")

def alert_on_lag(lag):
    """Simulate alerting (e.g., email/Slack for Wikimedia on-call)."""
    if lag > LAG_THRESHOLD_SEC:
        print(f"🚨 ALERT: Replication lag {lag}s exceeds {LAG_THRESHOLD_SEC}s threshold!")
        # TODO: Integrate with PagerDuty or Wikimedia's alerting
    else:
        print(f"✅ Lag OK: {lag}s")

def main():
    db = connect_db()
    try:
        lag = get_replication_lag(db)
        alert_on_lag(lag)
        topology = get_topology(db)
        print_topology_graph(topology)
    finally:
        db.close()

if __name__ == "__main__":
    main()
''',
    'scripts/schema_optimizer.py': '''#!/usr/bin/env python3
"""
MediaWiki Schema Optimizer - Analyzes queries/schemas for optimization.
Examples: Index suggestions for high-traffic tables like 'page' or 'category'.
Follows Wikimedia policies: Use unsigned ints, VARBINARY, batch writes.
"""

import pymysql
from config import DB_CONFIG

def connect_db():
    return pymysql.connect(**DB_CONFIG)

def analyze_query_performance(db, query):
    """Simulate EXPLAIN ANALYZE for optimization tips."""
    with db.cursor() as cursor:
        cursor.execute(f"EXPLAIN {query}")
        explain = cursor.fetchall()
        # Simple analysis: Check for full scans
        for row in explain:
            if 'ALL' in str(row):  # Full table scan
                print("⚠️  Optimization: Add index on scanned columns.")
        print("Query analyzed. Full output:", explain)

def suggest_schema_improvements(db, table_name):
    """Suggest Wikimedia-style improvements (e.g., from tables.json)."""
    with db.cursor() as cursor:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        tips = []
        for col in columns:
            field, type_, null, key, default, extra = col
            if 'int' in type_ and not 'unsigned' in type_:
                tips.append(f"💡 {field}: Use UNSIGNED INT to double capacity (Wikimedia policy).")
            if 'varchar' in type_:
                tips.append(f"💡 {field}: Consider VARBINARY for binary-safe storage.")
        print(f"Schema tips for {table_name}:")
        for tip in tips:
            print(tip)

# Example MediaWiki queries
SAMPLE_QUERY = "SELECT page_title FROM page WHERE page_namespace = 0 ORDER BY page_touched DESC LIMIT 10"
SAMPLE_TABLE = "page"  # Core MediaWiki table

def main():
    db = connect_db()
    try:
        analyze_query_performance(db, SAMPLE_QUERY)
        suggest_schema_improvements(db, SAMPLE_TABLE)
    finally:
        db.close()

if __name__ == "__main__":
    main()
''',
    'scripts/backup_validator.py': '''#!/usr/bin/env python3
"""
Backup Validator - Ensures reliable backups (Wikimedia: full coverage, automated recovery).
Simulates restore + checksum validation.
"""

import pymysql
import hashlib
from config import DB_CONFIG

def connect_db():
    return pymysql.connect(**DB_CONFIG)

def dump_and_checksum(db, table):
    """Dump table to string, compute checksum (simulate backup)."""
    with db.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        data_str = str(rows)
        return hashlib.md5(data_str.encode()).hexdigest()

def validate_backup(old_checksum, new_checksum):
    """Check if backup matches (for restore validation)."""
    if old_checksum == new_checksum:
        print("✅ Backup valid: Checksums match.")
    else:
        print("❌ Backup corrupted!")

def main():
    db = connect_db()
    try:
        checksum1 = dump_and_checksum(db, "page")  # Pre-backup
        # Simulate backup/restore here (e.g., mysqldump in prod)
        checksum2 = dump_and_checksum(db, "page")  # Post-restore
        validate_backup(checksum1, checksum2)
    finally:
        db.close()

if __name__ == "__main__":
    main()
''',
    'tests/test_replication.py': '''# Simple pytest for replication monitor
import pytest
from scripts.replication_monitor import get_replication_lag, alert_on_lag
from unittest.mock import Mock, patch

@pytest.fixture
def mock_db():
    db = Mock()
    db.cursor.return_value.fetchone.return_value = (None,) * 32 + (3,)  # Mock lag=3s
    return db

def test_lag_below_threshold(mock_db):
    with patch('pymysql.connect') as mock_connect:
        mock_connect.return_value = mock_db
        lag = get_replication_lag(mock_db)
        assert lag == 3
        alert_on_lag(lag)  # No alert expected

def test_lag_above_threshold():
    alert_on_lag(10)  # Should print alert
''',
    'docs/mariadb_wikimedia_notes.md': '''# Notes on Wikimedia's MariaDB Setup
- **Migration History**: Switched from MySQL to MariaDB in 2013 for open-source purity.
- **Scale**: ~50k QPS peak, 90% cached; uses semi-sync replication.
- **Lag Handling**: Avoid replicas >5s lag; batch writes, use waitForReplication().
- **Schema Best Practices**: Unsigned ints, VARBINARY, no ENUMs; abstract schema in tables.json.
- **Tools**: Orchestrator for topology viz; potential contrib area.
Sources: MediaWiki docs, Wikimedia blogs.
'''
}

# Create directories
os.makedirs('scripts', exist_ok=True)
os.makedirs('tests', exist_ok=True)
os.makedirs('docs', exist_ok=True)

# Write files
for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {filepath}")

print("Project files created. Run `git init`, `git add .`, and `git commit -m 'Initial commit'` to start.")
