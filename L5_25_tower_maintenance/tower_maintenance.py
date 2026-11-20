"""Track telecom tower maintenance, faults, and risk levels."""

import sqlite3

DB_CONNECTION = sqlite3.connect(":memory:")
DB_CONNECTION.execute(
    """
    CREATE TABLE towers (
        id INTEGER PRIMARY KEY,
        site TEXT,
        last_service INTEGER,
        faults INTEGER
    )
    """
)


def add_tower(site, last_service, faults=0):
    """Add a tower to the database."""
    DB_CONNECTION.execute(
        """
        INSERT INTO towers (site, last_service, faults)
        VALUES (?, ?, ?)
        """,
        (site, last_service, faults),
    )
    DB_CONNECTION.commit()


def service_tower(tower_id, year, service_count):
    """Record tower servicing and return the updated service count."""
    try:
        cursor = DB_CONNECTION.execute(
            """
            UPDATE towers
            SET last_service = ?, faults = 0
            WHERE id = ?
            """,
            (year, tower_id),
        )
        DB_CONNECTION.commit()
        if cursor.rowcount > 0:
            service_count += 1
    except sqlite3.Error as error:
        print(f"Service failed: {error}")
    return service_count


def overdue(year):
    """Return tower sites overdue for maintenance."""
    rows = DB_CONNECTION.execute(
        "SELECT site, last_service FROM towers"
    ).fetchall()
    return [
        site for site, last_service in rows
        if year - last_service >= 2
    ]


def risk_level(tower_id):
    """Return the risk category for a tower."""
    row = DB_CONNECTION.execute(
        "SELECT faults FROM towers WHERE id = ?",
        (tower_id,),
    ).fetchone()

    if row is None:
        return "unknown"
    if row[0] > 3:
        return "high"
    return "normal"


def snapshot():
    """Return a snapshot of all tower records."""
    return DB_CONNECTION.execute(
        "SELECT * FROM towers"
    ).fetchall()


def main():
    """Run a demonstration of the maintenance tracker."""
    service_count = 0
    add_tower("Ridge-A", 2021, 5)
    add_tower("Coast-B", 2024)
    service_count = service_tower(2, 2025, service_count)

    total = len(snapshot())
    print(overdue(2025), risk_level(1), total, service_count)


if __name__ == "__main__":
    main()
