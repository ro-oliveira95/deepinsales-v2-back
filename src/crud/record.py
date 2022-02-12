from typing import Optional
from db import db_instance

def get_record(record_id: str) -> dict:
  
  query = '''
    SELECT * FROM sales_records
    WHERE id = %s;
  '''

  data = (record_id,)

  record = db_instance.fetch_one(query, data)
  return record


def get_product_records(product_id: str, limit: Optional[int] = None) -> list:
  
  query = '''
    SELECT * FROM sales_records
    WHERE product_id = %s
    ORDER BY timestamp DESC;'''

  query = query[:-1] + f' LIMIT {limit};' if limit else query

  data = (product_id,)

  records = db_instance.fetch_many(query, data)
  return records

