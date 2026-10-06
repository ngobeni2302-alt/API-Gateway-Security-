from pydantic import BaseModel, Field, field_validator
import re


class WebhookPayload(BaseModel):
    event_id: str = Field(..., min_length=5, max_length=100)
    event_type: str = Field(..., min_length=2, max_length=50)
    timestamp: int = Field(..., gt=0)
    data: dict

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        # Prevent injection characters in event type
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", v):
            raise ValueError("Invalid characters detected in event_type")
        return v