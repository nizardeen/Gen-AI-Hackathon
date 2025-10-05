#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until pg_isready -U "$POSTGRES_USER" >/dev/null 2>&1; do
  echo "⏳ Waiting for PostgreSQL to start..."
  sleep 2
done

echo "✅ PostgreSQL is up. Creating database and importing CSV..."

# Create database
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE DATABASE hackathon;"

# Create table (assuming you have a SQL schema)
psql -U "$POSTGRES_USER" -d "hackathon" -f /sql/init_table.sql

# Import CSV into the table
psql -U "$POSTGRES_USER" -d "hackathon" -c "\COPY patient_record FROM '/data/personalized_medication_dataset.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';"

echo "🎉 Data import completed!"