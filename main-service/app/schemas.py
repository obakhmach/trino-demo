from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Final, List, Dict, Any
from enum import Enum


class TrinoExecutionStatuses(Enum):
    SUCCESS: Final[str] = "success"
    FAILED: Final[str] = "failed"


class Info(BaseModel):
    """Basic model to keep all the information about the app"""

    running: bool
    name: str
    version: str

    class Config:
        schema_extra = {
            "example": {
                "running": True,
                "appName": "An app name taken from the settings",
                "appVersion": "An app version taken from the settings",
            }
        }


class TrinoStatement(BaseModel):
    """Base model describing SQL statement that will
    be executed by the trino cluster in the JSON respresentation.
    """

    statement: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "statement": "SELECT user_id, form_id FROM mongo.test.users AS users"
            }
        }


class TrinoExecutionStatus(BaseModel):
    """Model to return the information about the trino execution status of
    a given statement"""

    status: str = Field(...)
    execution_id: str = Field(default=str(uuid4()), alias="executionId")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "executionId": "3859e43c-6b0f-4b13-bd91-baa8d1f3c0de",
            }
        }


class TrinoExecutionResult(BaseModel):
    """Model to keep all the execution result from trino cluster."""

    columns: List[Dict] = Field(...)
    data: List[List[Any]] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "columns": [
                    {
                        "name": "Catalog",
                        "type": "varchar(10)",
                        "typeSignature": {
                            "rawType": "varchar",
                            "arguments": [{"kind": "LONG", "value": 10}],
                        },
                    }
                ],
                "data": [["mongo"], ["postgresql"], ["system"], ["tpch"], ["tpchs"]],
            }
        }


class TrinoExecutionQueryResult(BaseModel):
    """Model to keep all results received from cached storage of the trino statement execution."""
