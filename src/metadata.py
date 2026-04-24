from config import *
from datetime import datetime

def get_last_id(cursor):

    cursor.execute("""
    SELECT last_id
    FROM pipeline_metadata
    WHERE pipeline_name=?
    """,
    PIPELINE_NAME)

    row=cursor.fetchone()

    return row[0] if row else 0


def update_metadata(
    cursor,
    last_id,
    status
):

    cursor.execute("""
    MERGE INTO pipeline_metadata AS target
    USING (SELECT ? pipeline_name) AS source
    ON target.pipeline_name=source.pipeline_name

    WHEN MATCHED THEN
      UPDATE SET
      last_id=?,
      last_run_time=?,
      status=?

    WHEN NOT MATCHED THEN
      INSERT (
      pipeline_name,
      last_id,
      last_run_time,
      status
      )
      VALUES (?,?,?,?)
    """,
    PIPELINE_NAME,
    last_id,
    datetime.now(),
    status,
    PIPELINE_NAME,
    last_id,
    datetime.now(),
    status
    )