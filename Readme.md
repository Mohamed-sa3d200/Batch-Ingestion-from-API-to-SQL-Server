# 📊 Production-Grade Data Pipeline: API to SQL Server

## 🧠 Overview

This project simulates a real-world **data engineering pipeline** that extracts data from a REST API and loads it into SQL Server using production-grade design patterns.

The pipeline includes:

- API ingestion
- Incremental loading
- Pagination handling
- Retry logic for API failures
- Upsert processing with SQL Server MERGE
- Metadata-driven state tracking
- Logging and error handling
- Modular project structure

The goal is to model how pipelines are built in enterprise environments.

---

# 🏗️ Architecture

```text
REST API
   ↓
API Client
   ↓
Python Pipeline
   ↓
SQL Server
   ↓
Metadata Table
```

---

# 🎯 Key Features

- ✅ Incremental Data Loading  
- ✅ Idempotent Processing  
- ✅ Pagination Support  
- ✅ Retry Mechanism  
- ✅ SQL Server MERGE Upserts  
- ✅ Metadata State Tracking  
- ✅ Logging & Error Handling  
- ✅ Modular Repository Structure  
- ✅ Fault-Tolerant Design

---

# 📁 Repository Structure

```text
api-to-sqlserver-pipeline/

src/
├── main.py
├── config.py
├── db.py
├── api_client.py
├── loader.py
├── metadata.py
└── logger.py

sql/
├── create_posts_table.txt
└── create_metadata_table.txt

logs/
└── pipeline.log

requirements.txt
README.md
.gitignore
```

---

# 🧱 Step 1: Database Design

## Main Table

```sql
CREATE TABLE posts (
    id INT PRIMARY KEY,
    user_id INT,
    title NVARCHAR(255),
    body NVARCHAR(MAX)
);
```

---

## Metadata Table

```sql
CREATE TABLE pipeline_metadata (
    pipeline_name NVARCHAR(100),
    last_run_time DATETIME2,
    last_id INT,
    status NVARCHAR(50),
    PRIMARY KEY (pipeline_name)
);
```

---

# 🧠 Why Use a Metadata Table?

Instead of relying only on:

```sql
SELECT MAX(id) FROM posts;
```

We persist pipeline state explicitly:

- last processed record (`last_id`)
- last run timestamp
- run status (SUCCESS / FAILED)

Benefits:

- Recovery after failure  
- No duplicate processing  
- Better observability  
- Reliable restart point

---

# 🔄 Incremental Load Strategy

Because the API does not provide `last_updated`,
incremental loading is simulated using:

```text
Load records where id > last_id
```

---

# 🌐 Data Extraction

API used:

```http
https://jsonplaceholder.typicode.com/posts
```

Basic extraction:

```python
response = requests.get(url)
response.raise_for_status()
data = response.json()
```

---

# 📄 Pagination Handling

The API is queried page by page:

```python
while True:

    url = (
      f"{API_URL}"
      f"?_page={page}"
      f"&_limit={PAGE_SIZE}"
    )

    data = fetch_with_retry(url)

    if not data:
        break

    all_records.extend(data)

    page += 1
```

## Why Pagination?

Without it:

- Data loss can occur  
- Only first page would be loaded

---

# 🔁 Retry Mechanism

Transient API failures are handled with retries.

```python
for attempt in range(MAX_RETRIES):

    try:
        response=requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception:

        time.sleep(2)
```

## Why Retry?

Protects against:

- Timeouts  
- Temporary network failures  
- 500-level server errors

---

# 🔍 Filtering New Records

```python
new_records = [
  post for post in data
  if post["id"] > last_id
]
```

This prevents:

- Duplicate loads  
- Unnecessary processing

---

# 🔁 Upsert Logic (MERGE)

```sql
MERGE INTO posts AS target

USING (
 SELECT ? id,
        ? user_id,
        ? title,
        ? body
) AS source

ON target.id=source.id

WHEN MATCHED THEN
 UPDATE SET
 user_id=source.user_id,
 title=source.title,
 body=source.body

WHEN NOT MATCHED THEN
 INSERT (
   id,
   user_id,
   title,
   body
 )
 VALUES(
   source.id,
   source.user_id,
   source.title,
   source.body
 );
```

## Why MERGE?

- Insert new records  
- Update existing records  
- Ensure idempotency

---

# 🧾 Metadata Management

Read pipeline state:

```sql
SELECT last_id
FROM pipeline_metadata
WHERE pipeline_name='posts_pipeline';
```

Update state:

- On success → update last_id and status  
- On failure → preserve state for recovery

---

# 🪵 Logging

```python
logging.info("Pipeline started")
logging.error("Pipeline failed")
```

Used for:

- Debugging  
- Monitoring  
- Auditing

---

# ⚠️ Error Handling

```python
try:
   run_pipeline()

except Exception as e:

   logging.error(str(e))

   conn.rollback()

   raise
```

Provides:

- Failure capture  
- Safe rollback  
- Recovery support

---

# 🔁 Pipeline Flow

Each pipeline run:

1. Read last_id from metadata  
2. Fetch paginated data  
3. Apply retry-protected API calls  
4. Filter new records  
5. Upsert into SQL Server  
6. Update metadata  
7. Commit transaction  

---

# 🧠 Core Data Engineering Concepts

## Idempotency
Re-running produces same result.

---

## Incremental Processing
Only new records are processed.

---

## State Management
Metadata stores pipeline progress.

---

## Fault Tolerance
Pipeline survives failures.

---

## Resilience
Retry handles temporary outages.

---

# 🚀 Future Improvements

Possible extensions:

- Scheduling with Apache Airflow
- Environment variable secrets
- Unit tests with pytest
- Monitoring and alerts
- Dead-letter handling
- Cloud deployment

---

# 🏁 Conclusion

This project demonstrates core production data engineering patterns:

- API ingestion  
- Incremental loading  
- Pagination  
- Retry logic  
- MERGE upserts  
- Metadata tracking  
- Fault tolerance  
- Modular design

These patterns are transferable to enterprise tools such as:

- Apache Airflow  
- dbt  
- Snowflake  
- Cloud data platforms
