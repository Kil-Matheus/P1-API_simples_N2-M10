# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Environment variables for PostgreSQL
ENV POSTGRES_USER = postgres
ENV POSTGRES_PASSWORD = postgres
ENV POSTGRES_DB = postgres

# Copy the SQL script to initialize the database
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5433