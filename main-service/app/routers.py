from fastapi import APIRouter, Body, Depends
from typing import Dict
from redis.asyncio import Redis
from uuid import uuid4

from app.services import (
    execute_trino_sql_statement as execute_trino_sql_statement_service,
    get_execution_query_result as get_execution_query_result_service,
)
from app.schemas import (
    Info as InfoSchema,
    TrinoExecutionStatus as TrinoExecutionStatusSchema,
    TrinoStatement as TrinoStatementSchema,
    TrinoExecutionResult as TrinoExecutionResultSchema,
)
from app.settings import settings
from app.dependencies import get_redis

router = APIRouter()


@router.get(
    "/",
    response_model=InfoSchema,
    tags=["index"],
)
async def index() -> InfoSchema:
    """Return the list of the all available videos to view."""
    return InfoSchema(
        running=True, name=settings.app_name, version=settings.app_version
    )


@router.post(
    "/trino/statements/Execute",
    response_model=TrinoExecutionStatusSchema,
    tags=["trino"],
)
async def trino_status(
    trino_statement_schema: TrinoStatementSchema = Body(...),
    redis_client: Redis = Depends(get_redis),
) -> TrinoExecutionStatusSchema:
    """Return the basic information about the trino cluster configuration status."""
    return await execute_trino_sql_statement_service(
        redis_client, trino_statement_schema.statement
    )


@router.get(
    "/trino/statements/executions/{execution_id}/{execution_set}",
    response_model=TrinoExecutionResultSchema,
    tags=["trino"],
)
async def trino_execution_query_result(
    execution_id: str, execution_set: int, redis_client: Redis = Depends(get_redis)
) -> TrinoExecutionResultSchema:
    """Return the part of the results of the exeution cahced under the given execution_id."""
    return await get_execution_query_result_service(
        redis_client, execution_id, execution_set
    )
