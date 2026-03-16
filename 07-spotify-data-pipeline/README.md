# Spotify Data Engineering Pipeline

An end-to-end Big Data pipeline utilizing the **Medallion Architecture** to process 1.2M records.

## Tech Stack
* **Compute:** PySpark on Google Dataproc Serverless
* **Storage:** Google Cloud Storage (GCS)
* **Warehouse:** BigQuery
* **Orchestration:** Spark Connect

## Key Engineering Challenges
* **Schema Drift:** Handled malformed CSV data (column shifting) where strings like 'opera' appeared in numeric columns.
* **Defensive Cleansing:** Implemented `try_cast` logic in Spark SQL to ensure pipeline resilience and 99%+ data retention.
* **Optimization:** Materialized a "Silver" layer in BigQuery to convert raw strings into optimized numeric types for high-speed analytics.
