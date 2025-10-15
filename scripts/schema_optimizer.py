#!/usr/bin/env python3
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
