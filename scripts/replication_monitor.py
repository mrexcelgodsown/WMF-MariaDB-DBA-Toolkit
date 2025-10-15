#!/usr/bin/env python3
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
