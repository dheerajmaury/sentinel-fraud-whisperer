from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FullFeedback(BaseModel):
    transaction_id: str
    is_correct: bool
    feedback: str
    reason: Optional[str] = None
    timestamp: datetime



