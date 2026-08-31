import sqlite3

def connect_db():
    """Establish and return SQLite connection."""
    conn = sqlite3.connect("fleet_maintenance.db")
    return conn

def init_schema(cursor):
    """Create tables according to the relational schema."""
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS trains (
        train_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        train_type TEXT NOT NULL CHECK(train_type IN ('Electric', 'Diesel-Electric', 'High-Speed')),
        status TEXT NOT NULL DEFAULT 'Active'
    );

    CREATE TABLE IF NOT EXISTS maintenance_depots (
        depot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        depot_name TEXT NOT NULL,
        location TEXT NOT NULL,
        capacity INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS maintenance_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_id INTEGER NOT NULL,
        depot_id INTEGER NOT NULL,
        service_type TEXT NOT NULL,
        cost REAL NOT NULL,
        log_date TEXT NOT NULL,
        FOREIGN KEY (train_id) REFERENCES trains(train_id) ON DELETE CASCADE,
        FOREIGN KEY (depot_id) REFERENCES maintenance_depots(depot_id) ON DELETE CASCADE
    );
    """)

def insert_records(cursor):
    """Seed initial data records for fleet operations."""
    trains = [
        ("Series 8000 EMU", "Electric", "Active"),
        ("GE C30-7 Diesel", "Diesel-Electric", "Under Maintenance"),
        ("Shinkansen E5", "High-Speed", "Active"),
        ("Rotem DMU", "Diesel-Electric", "Active")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO trains (model_name, train_type, status) VALUES (?, ?, ?);",
        trains
    )

    depots = [
        ("Tutuban Central Yard", "Manila", 12),
        ("Caloocan Maintenance Hub", "Caloocan", 8),
        ("Clark Depot Facility", "Pampanga", 15)
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO maintenance_depots (depot_name, location, capacity) VALUES (?, ?, ?);",
        depots
    )

    logs = [
        (1, 1, "Brake Pad Replacement", 45000.00, "2026-07-15"),
        (2, 2, "Engine Overhaul", 185000.00, "2026-08-01"),
        (3, 3, "Pantograph Inspection", 32000.00, "2026-08-10"),
        (4, 1, "HVAC Maintenance", 18000.00, "2026-08-18"),
        (2, 2, "Traction Motor Servicing", 92000.00, "2026-08-22")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO maintenance_logs (train_id, depot_id, service_type, cost, log_date) VALUES (?, ?, ?, ?, ?);",
        logs
    )

def view_all_logs(cursor):
    print("\n" + "=" * 80)
    print("MAINTENANCE LOGS (MULTI-TABLE JOIN)")
    print("=" * 80)
    cursor.execute("""
        SELECT ml.log_id, t.model_name, t.train_type, d.depot_name, ml.service_type, ml.cost, ml.log_date
        FROM maintenance_logs ml
        JOIN trains t ON ml.train_id = t.train_id
        JOIN maintenance_depots d ON ml.depot_id = d.depot_id
        ORDER BY ml.log_date DESC;
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Log #{row[0]} | {row[1]} ({row[2]}) | Depot: {row[3]} | Service: {row[4]} | PHP {row[5]:,.2f} | Date: {row[6]}")

def view_filtered_logs(cursor):
    print("\n" + "=" * 70)
    print("HIGH-COST MAINTENANCE FILTER (WHERE cost >= PHP 40,000)")
    print("=" * 70)
    cursor.execute("""
        SELECT t.model_name, ml.service_type, ml.cost, ml.log_date
        FROM maintenance_logs ml
        JOIN trains t ON ml.train_id = t.train_id
        WHERE ml.cost >= 40000.00
        ORDER BY ml.cost DESC;
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Train: {row[0]:<20} | Service: {row[1]:<25} | Cost: PHP {row[2]:,.2f} | Date: {row[3]}")

def view_depot_summary(cursor):
    print("\n" + "=" * 70)
    print("DEPOT MAINTENANCE SUMMARY (GROUP BY & AGGREGATION)")
    print("=" * 70)
    cursor.execute("""
        SELECT d.depot_name, d.location, COUNT(ml.log_id) AS total_jobs, COALESCE(SUM(ml.cost), 0.0) AS total_spent
        FROM maintenance_depots d
        LEFT JOIN maintenance_logs ml ON d.depot_id = ml.depot_id
        GROUP BY d.depot_id;
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Depot: {row[0]:<26} | Loc: {row[1]:<10} | Jobs: {row[2]} | Total Spend: PHP {row[3]:,.2f}")

def log_new_service(cursor, conn):
    print("\n--- LOG NEW MAINTENANCE SERVICE ---")
    
    print("\nAvailable Trains:")
    cursor.execute("SELECT train_id, model_name, status FROM trains;")
    for row in cursor.fetchall():
        print(f"[{row[0]}] {row[1]} - Status: {row[2]}")
    train_id = input("Select Train ID: ").strip()

    print("\nAvailable Depots:")
    cursor.execute("SELECT depot_id, depot_name, location FROM maintenance_depots;")
    for row in cursor.fetchall():
        print(f"[{row[0]}] {row[1]} ({row[2]})")
    depot_id = input("Select Depot ID: ").strip()

    service_type = input("Enter Service Type (e.g., Oil Change): ").strip()
    cost = input("Enter Service Cost (PHP): ").strip()
    log_date = input("Enter Log Date (YYYY-MM-DD): ").strip()

    try:
        cursor.execute("""
            INSERT INTO maintenance_logs (train_id, depot_id, service_type, cost, log_date)
            VALUES (?, ?, ?, ?, ?);
        """, (int(train_id), int(depot_id), service_type, float(cost), log_date))
        conn.commit()
        print("\nService log added successfully!")
    except Exception as e:
        print(f"\nError logging service: {e}")

def ask_return_to_menu():
    """Ask user whether they want to return to the main menu or exit."""
    while True:
        choice = input("\nDo you want to go back to the menu? (y/n): ").strip().lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def main():
    conn = connect_db()
    cursor = conn.cursor()

    init_schema(cursor)
    insert_records(cursor)
    conn.commit()

    while True:
        print("\n" + "=" * 45)
        print("  FLEET MAINTENANCE MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. View All Maintenance Logs (Multi-Table JOIN)")
        print("2. View High-Cost Records (WHERE Filter)")
        print("3. View Depot Summary (GROUP BY Summary)")
        print("4. Log New Maintenance Service")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            view_all_logs(cursor)
        elif choice == "2":
            view_filtered_logs(cursor)
        elif choice == "3":
            view_depot_summary(cursor)
        elif choice == "4":
            log_new_service(cursor, conn)
        elif choice == "5":
            print("\nExiting fleet maintenance system. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1-5.")

        # Prompt user after completing any action (1-4 or invalid choice)
        if not ask_return_to_menu():
            print("\nExiting fleet maintenance system. Goodbye!")
            break

    conn.close()

if __name__ == "__main__":
    main()