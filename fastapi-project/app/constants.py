from fastapi import HTTPException

error = HTTPException(status_code=404, detail="Todo not found")