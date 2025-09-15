from pydantic import BaseModel
from datetime import datetime

class ExampleBase(BaseModel):
    title: str
    content: str | None = None

class Example(ExampleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ExampleCreate(ExampleBase):
    pass

class ExampleUpdate(ExampleBase):
    pass

class ExampleDelete(ExampleBase):
    id: int
