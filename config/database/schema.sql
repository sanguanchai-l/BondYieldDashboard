-- Bond Yield Database Schema
-- For storing 10-year government bond yields (Nominal and Real)

-- Main table for bond yield data
CREATE TABLE IF NOT EXISTS bond_yields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,           -- 'thailand' or 'us'
    date DATE NOT NULL,
    nominal_yield REAL,              -- 10-year nominal yield (%)
    real_yield REAL,                 -- 10-year real yield / TIPS (%)
    difference REAL,                 -- Spread (nominal - real) in basis points
    data_source TEXT,                -- Source of data (FRED, Investing, etc.)
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(country, date)
);

-- Update log for tracking data freshness
CREATE TABLE IF NOT EXISTS update_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    last_update DATE,                -- Latest date in database
    last_fetch TIMESTAMP,            -- Last API call time
    record_count INTEGER,            -- Total records for this country
    status TEXT,                     -- 'success', 'failed', 'partial'
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_country_date ON bond_yields(country, date);
CREATE INDEX IF NOT EXISTS idx_date ON bond_yields(date);
CREATE INDEX IF NOT EXISTS idx_country ON bond_yields(country);
