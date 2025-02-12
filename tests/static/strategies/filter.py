"""Filter test strategy class."""
# pylint: disable=unused-argument
from typing import TYPE_CHECKING

from pydantic.dataclasses import dataclass

from oteapi.models import FilterConfig

if TYPE_CHECKING:
    from typing import Any, Dict, Optional


@dataclass
class FilterTestStrategy:
    """Test filter strategy."""

    filter_config: FilterConfig

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize."""
        return {}

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run filter strategy."""
        return {}
