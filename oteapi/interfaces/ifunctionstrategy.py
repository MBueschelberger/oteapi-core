"""Function Strategy Interface"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

    from oteapi.models import FunctionConfig, FunctionStatus


@dataclass  # type: ignore[misc]
@runtime_checkable
class IFunctionStrategy(Protocol):
    """Function Strategy Interface."""

    function_config: "FunctionConfig"

    def run(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Run a function job.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.
            As a minimum, the dictionary will contain the job ID.

        """

    def status(self, task_id: str) -> "FunctionStatus":
        """Get job status.

        Parameters:
            task_id: The function job ID.

        Returns:
            An overview of the function job's status, including relevant
            metadata.

        """

    def get(self, session: "Optional[Dict[str, Any]]" = None) -> "Dict[str, Any]":
        """Execute the strategy.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """

    def initialize(
        self, session: "Optional[Dict[str, Any]]" = None
    ) -> "Dict[str, Any]":
        """Initialize data class.

        This method will be called through the `/initialize` endpoint of the OTE-API
        Services.

        Parameters:
            session: A session-specific dictionary context.

        Returns:
            Dictionary of key/value-pairs to be stored in the sessions-specific
            dictionary context.

        """
