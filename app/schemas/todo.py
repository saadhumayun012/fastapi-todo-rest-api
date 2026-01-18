from pydantic import BaseModel, Field

#TodoRequest
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int
    complete: bool = Field(default=False)