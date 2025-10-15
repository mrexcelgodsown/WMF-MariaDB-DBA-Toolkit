# WMF MariaDB DBA Toolkit

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
