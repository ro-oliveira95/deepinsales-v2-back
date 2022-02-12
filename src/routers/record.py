from typing import Optional
from fastapi import APIRouter, Depends
from crud import record

router = APIRouter(
  prefix='/records',
  tags=['records'],
  # dependencies=[Depends(verify_token)],
  responses={404: {'Description': 'Not Found'}},
)

@router.get('/{product_id}', status_code=200)
def get_product_records(product_id: str, limit: Optional[int] = None):
  records = record.get_product_records(product_id, limit)
  return {
    "product_id": product_id,
    "records": records
  }