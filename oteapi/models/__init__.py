"""`oteapi.models` module.

This module contains all the `pydantic` configuration models.
"""
from typing import Union

from .datacacheconfig import DataCacheConfig
from .filterconfig import FilterConfig
from .functionconfig import FunctionConfig, FunctionStatus
from .mappingconfig import MappingConfig
from .resourceconfig import ResourceConfig
from .transformationconfig import TransformationConfig, TransformationStatus

__all__ = (
    "DataCacheConfig",
    "FilterConfig",
    "FunctionConfig",
    "FunctionStatus",
    "MappingConfig",
    "ResourceConfig",
    "StrategyConfig",
    "TransformationConfig",
    "TransformationStatus",
)

StrategyConfig = Union[
    FilterConfig, FunctionConfig, MappingConfig, ResourceConfig, TransformationConfig
]
