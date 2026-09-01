# CPE106L-4: Laboratory Activity 6 - OpenGauss*

*since OpenGauss is not available, SQL was instead used.

## Project Overview

This laboratory activity implements a Relational Database Model using SQL and Python's built-in `sqlite3` interface.
The system models a railway fleet maintenance and depot tracking system (**Yuan's Train Fleet Maintenance Operations**) where fleet units, maintenance facilities, and service logs are managed with relational integrity and multi-table queries.

## Relational Schema Design

* **`trains`**: Stores fleet assets, propulsion types (`Electric`, `Diesel-Electric`, `High-Speed`), and operational status (`Active`, `Under Maintenance`).
* **`maintenance_depots`**: Tracks maintenance facilities, regional locations, and capacity limits.
* **`maintenance_logs`**: Junction/transaction entity recording service jobs, associated train and depot IDs, expenditures, and service dates with foreign key constraints.

## SQL Query Implementation

1. **Multi-Table Join (`JOIN`)**: Aggregates comprehensive maintenance records with train models, depot locations, and service details.
2. **Filtered Query (`WHERE`)**: Filters high-value maintenance jobs exceeding PHP 40,000.00.
3. **Aggregation & Grouping (`GROUP BY`, `SUM`, `COUNT`)**: Calculates total servicing jobs and cumulative maintenance expenditure per depot facility.

## Project Structure

```text
velasco_danielyuan_labactivity6/
├── screenshots/         # Terminal test execution evidence
│   └── test_case_lab6_screenshots.pdf
├── src/
│   └── main.py          # SQLite database connection, schema setup, record seeding, and queries
├── schema.sql           # Database schema definition script
└── README.md            # Activity documentation and run instructions
```

## How to Run

1. Open your Ubuntu WSL terminal and navigate to the project directory:
```bash
cd velasco_danielyuan_labactivity6
```

2. Run the application:
```bash
python3 src/main.py
```

## AI Disclosure

AI assistant (Gemini) was used to assist in schema structure design, query formatting, and debugging during the development of this project.