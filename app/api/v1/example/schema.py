from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ExampleBase(BaseModel):
    title: str
    content: str | None = None

class Example(ExampleBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExampleCreate(ExampleBase):
    pass

class ExampleUpdate(ExampleBase):
    pass

class ExampleDelete(ExampleBase):
    id: int
