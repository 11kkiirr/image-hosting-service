from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )


class TimestampReadSchema(BaseSchema):
    created_at: datetime | None
    updated_at: datetime | None
