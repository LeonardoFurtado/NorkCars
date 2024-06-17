#!/bin/sh

# Wait for the PostgreSQL database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h db -p 5432 -q; do
  sleep 1
done

# Run the database migrations
flask db upgrade

# Start the Flask application
exec flask run --host=0.0.0.0
