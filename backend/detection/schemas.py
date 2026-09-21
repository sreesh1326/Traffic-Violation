from pydantic import BaseModel
from typing import List
from datetime import datetime

class ViolationResult(BaseModel):
    violation_type: str
    confidence: float
    timestamp: datetime

class DetectionResult(BaseModel):
    annotated_image: str
    violations: List[ViolationResult]
    timestamp: datetime

