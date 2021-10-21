"""
Transformation Plugin that use the Celery framework to call remote workers
"""
#pylint: disable=W0613, W0511
from app.strategy.factory import StrategyFactory
from pydantic import BaseModel
from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from fastapi_plugins import RedisSettings
from app.models.transformationconfig import TransformationConfig, TransformationStatus
from celery import Celery
from celery.result import AsyncResult


# Connect Celery to the currently running Reddis instance
app = Celery(broker=RedisSettings().redis_url, backend=RedisSettings().redis_url)


class CeleryConfig(BaseModel):
    taskName: str
    args: List[Any]

@dataclass
@StrategyFactory.register(
    ('transformation_type', 'celery/remote')
)
class CeleryRemoteStrategy:
    """ Submit job to remote runner """

    transformation_config: TransformationConfig

    def run(self, session_id: Optional[str] = None) -> Dict:
        """ Run a job, return a jobid"""

        config = self.transformation_config.configuration
        celeryConfig = CeleryConfig(**config)
        result = app.send_task(celeryConfig.taskName, celeryConfig.args)
        return dict(result=result.task_id)

    def initialize(self, session: Optional[Dict[str, Any]] = None) -> Dict:
        """ Initialize a job"""
        return dict()

    def status(self, task_id: str) -> TransformationStatus:
        """ Get job status """
        result = AsyncResult(id=task_id, app=app)
        ts = TransformationStatus(
            id=task_id,
            status=result.state
        )
        return ts

    def get(self, session_id: Optional[str] = None) -> Dict:
        """ get transformation """

        # TODO: update and return global state
        return dict()
