def upsert_post(cursor,post):

    cursor.execute("""
    MERGE INTO posts AS target

    USING (
      SELECT
      ? id,
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
      INSERT(
      id,user_id,title,body
      )
      VALUES(
      source.id,
      source.user_id,
      source.title,
      source.body
      )
    """,

    post["id"],
    post["userId"],
    post["title"],
    post["body"]
    )