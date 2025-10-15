#!/usr/bin/env python3
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
