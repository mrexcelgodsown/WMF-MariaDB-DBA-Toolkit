# Notes on Wikimedia's MariaDB Setup
- **Migration History**: Switched from MySQL to MariaDB in 2013 for open-source purity.
- **Scale**: ~50k QPS peak, 90% cached; uses semi-sync replication.
- **Lag Handling**: Avoid replicas >5s lag; batch writes, use waitForReplication().
- **Schema Best Practices**: Unsigned ints, VARBINARY, no ENUMs; abstract schema in tables.json.
- **Tools**: Orchestrator for topology viz; potential contrib area.
Sources: MediaWiki docs, Wikimedia blogs.
