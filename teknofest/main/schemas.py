from pydantic import BaseModel
from typing import List


class Column(BaseModel):
    name: str


class Table(BaseModel):
    name: str
    columns: List[Column]


class DatabaseMetadata(BaseModel):
    table: List[Table]
