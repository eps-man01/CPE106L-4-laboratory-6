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