from datetime import datetime
from pydantic import BaseModel

class Record(BaseModel):
  id: str
  total_sells: int  
  total_visits: int
  daily_sells: int
  daily_visits: int
  product_id: str
  timestamp: datetime