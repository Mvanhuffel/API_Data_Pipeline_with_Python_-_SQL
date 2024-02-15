# API Data Pipeline with Python, SQL, and dbt

*In Progress*

```ruby
API_Pipeline_Python_SQL_dbt/
│
├── README.md                   # Project overview and setup instructions
│
├── requirements.txt            # Python dependencies for the project
│
├── .env.example                # Template for environment variables
│
├── .gitignore                  # Untracked files to ignore
│
├── db/                         # Database-related scripts and schemas
│   ├── init/                   # Initialization scripts for database setup
│   │   └── schema.sql          # SQL script to create database schema
│   │
│   ├── migrations/             # Database migration scripts
│   │   └── V1__initial_structure.sql  # Versioned migration script
│   │
│   └── curation/               # SQL scripts for data transformation and curation
│       ├── aggregate_data.sql  # Example aggregation script
│       └── clean_data.sql      # Data cleaning script
│
├── src/                        # Source code for the project
│   ├── config/                 # Configuration files and scripts
│   │   └── db_config.py        # Database configuration settings
│   │
│   └── main.py                 # Main script for running the data pipeline
│
├── tests/                      # Test cases for the project
│   ├── test_db.py              # Tests for database operations
│   └── test_api.py             # Tests for API data fetching
```