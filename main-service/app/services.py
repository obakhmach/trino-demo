import json

from typing import Dict, List, Any
from httpx import AsyncClient, Response
from redis.asyncio import Redis

from app.settings import settings
from app.schemas import TrinoExecutionStatus as TrinoExecutionStatusSchema
from app.schemas import TrinoExecutionResult as TrinoExecutionResultSchema
from app.schemas import TrinoExecutionResultCount as TrinoExecutionResultCountSchema
from app.schemas import TrinoExecutionStatuses


async def get_execution_query_result_count(redis_client: Redis, execution_id: str) -> TrinoExecutionResultCountSchema:
    """Query a Redis cache storage to find query result count corresponding given execution id and
    execution set.

    Args:
        execution_id: An id of the hash map inside redis where related results were cahced.
        redis_client: Async client to access redis cache storage.

    Returns:
        Number of sets cached after execution
    """
    query_result_exists: bool = bool(await redis_client.exists(execution_id))

    if not query_result_exists:
        raise Exception("Exception results are not preset.")

    query_result_set_count: int = await redis_client.hlen(execution_id)

    return TrinoExecutionResultCountSchema(count=query_result_set_count)


async def get_execution_query_result(
    redis_client: Redis, execution_id: str, execution_set: int
) -> TrinoExecutionResultSchema:
    """Query a Redis cache storage to find query result corresponding given execution id and
    execution set.

    Args:
        execution_id: An id of the hash map inside redis where related results were cahced.
        execution_set: Corresponding index of the part of results were cached.
        redis_client: Async client to access redis cache storage.

    Returns:
        Part of results of a trino statements chich was cached under the execution id.
    """
    query_result_exists: bool = bool(await redis_client.exists(execution_id))

    if not query_result_exists:
        raise Exception("Exception results are not preset.")

    query_result_set_count: int = await redis_client.hlen(execution_id)

    if execution_set + 1 > query_result_set_count:
        raise Exception("Current execution set number is too big.")

    cached_execution_query_result_part = await redis_client.hget(
        execution_id, execution_set
    )

    return TrinoExecutionResultSchema(**json.loads(cached_execution_query_result_part))


async def execute_trino_sql_statement(
    redis_client: Redis, sql_statement: str
) -> TrinoExecutionStatusSchema:
    """Make a get request to main trino coordinator to get the
    main cluster information.

    Args:
        redis_client: Async client to access redis cache storage.
        sql_statement: A valid sql statement that will be executed on the trino cluser
                       involving all the connectors descived. For more information
                       about sql statements that can be executed on the trino cluser please
                       look trino official docs.

    Returns:
        Information about whole execution process and the id if process was successfull where result will be cahced.
    """
    trino_execution_status: TrinoExecutionStatusSchema = TrinoExecutionStatusSchema(
        status=TrinoExecutionStatuses.FAILED.value
    )

    trino_statement_execution_uri: str = (
        f"{settings.trino_coordinator_url}/v1/statement"
    )
    # This type of header is requeired by trino without any authorization configured.
    trino_status_information_headers: Dict = {"X-Trino-User": settings.app_name}
    trino_exeution_set_counter: int = 0

    try:
        async with AsyncClient() as client:
            trino_status_information_response: Response = await client.post(
                url=trino_statement_execution_uri,
                headers=trino_status_information_headers,
                data=sql_statement.encode(),
            )

        trino_status_information: Dict = trino_status_information_response.json()
        trino_statement_execution_next_uri: str = trino_status_information.get(
            "nextUri"
        )

        while trino_statement_execution_next_uri is not None:
            async with AsyncClient() as client:
                trino_status_information_response: Response = await client.get(
                    url=trino_statement_execution_next_uri,
                    headers=trino_status_information_headers,
                )

            trino_status_information: Dict = trino_status_information_response.json()
            trino_statement_execution_next_uri: str = trino_status_information.get(
                "nextUri"
            )

            columns: List[Dict] = trino_status_information.get("columns")
            data: List[List[Any]] = trino_status_information.get("data")
            error: Dict = trino_status_information.get("error")

            if error is not None:
                raise Exception("Trino query failed.")

            if columns is not None and data is not None:
                trino_execution_result = TrinoExecutionResultSchema(
                    columns=columns, data=data
                )

                print(trino_exeution_set_counter)

                await redis_client.hset(
                    trino_execution_status.execution_id,
                    trino_exeution_set_counter,
                    trino_execution_result.json(),
                )

                trino_exeution_set_counter += 1

        trino_execution_status.status = TrinoExecutionStatuses.SUCCESS.value

    except Exception as e:
        pass

    return trino_execution_status
