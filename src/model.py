from pydantic import BaseModel
from typing import Dict


class HTreeFilter(BaseModel):
    rectangle: list[float]
    cluster_id: int
