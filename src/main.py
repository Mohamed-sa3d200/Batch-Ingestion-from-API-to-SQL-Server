from db import get_connection
from api_client import fetch_paginated_data
from metadata import (
 get_last_id,
 update_metadata
)
from loader import upsert_post
from logger import logger

def run_pipeline():

    conn=get_connection()

    cursor=conn.cursor()

    try:

        last_id=get_last_id(cursor)

        data=fetch_paginated_data()

        new_records=[
            x for x in data
            if x["id"] > last_id
        ]

        for post in new_records:
            upsert_post(
                cursor,
                post
            )

        if new_records:
            max_id=max(
              p["id"]
              for p in new_records
            )
        else:
            max_id=last_id

        update_metadata(
            cursor,
            max_id,
            "SUCCESS"
        )

        conn.commit()

        logger.info(
          "Pipeline success"
        )

    except Exception as e:

        logger.error(str(e))

        conn.rollback()

        raise

    finally:

        conn.close()


if __name__=="__main__":
    run_pipeline()