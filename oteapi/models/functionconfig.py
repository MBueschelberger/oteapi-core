"""Pydantic Function Configuration Data Model.

A function status data model is provided as well.
This data model represents what should be returned from the strategy's `status()`
method.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class PriorityEnum(str, Enum):
    """Defining process priority enumerators.

    Process priorities:

    - Low
    - Medium
    - High

    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class FunctionConfig(BaseModel):
    """Function Strategy Data Configuration."""

    function_type: str = Field(
        ...,
        description=("Type of registered function strategy. E.g., `python/my_func`."),
    )
    name: Optional[str] = Field(
        None, description="Human-readable name of the function strategy."
    )
    description: Optional[str] = Field(
        None, description="A free-text account of the function."
    )
    due: Optional[datetime] = Field(
        None,
        description=(
            "Optional field to indicate a due data/time for when a function "
            "should finish."
        ),
    )
    priority: Optional[PriorityEnum] = Field(
        PriorityEnum.MEDIUM,
        description="Define the process priority of the function execution.",
    )
    secret: Optional[str] = Field(
        None,
        description="Authorization secret given when running a function.",
    )
    configuration: Optional[dict] = Field(
        None,
        description=(
            "Function-specific configuration options given as key/value-pairs."
        ),
    )


class FunctionStatus(BaseModel):
    """Return from function status."""

    id: str = Field(..., description="ID for the given function process.")
    status: Optional[str] = Field(None, description="Status for the function process.")
    messages: Optional[List[str]] = Field(
        None, description="Messages related to the function process."
    )
    created: Optional[datetime] = Field(
        None,
        description="Time of creation for the function process. Given in UTC.",
    )
    startTime: Optional[datetime] = Field(
        None, description="Time when the function process started. Given in UTC."
    )
    finishTime: Optional[datetime] = Field(
        None, description="Time when the tranformation process finished. Given in UTC."
    )
