"""Airtable API client with async HTTP support."""

import os
import httpx

BASE_URL = "https://api.airtable.com/v0"


class AirtableError(Exception):
    """Base exception for Airtable operations."""
    pass


class AirtableClient:
    """Async client for the Airtable Web API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("AIRTABLE_API_KEY")
        if not self.api_key:
            raise AirtableError(
                "AIRTABLE_API_KEY environment variable is required. "
                "Get your API key at https://airtable.com/create/tokens"
            )
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=BASE_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
        return self._client

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    def _handle_error(self, response: httpx.Response) -> None:
        """Raise helpful errors for non-2xx responses."""
        if response.status_code == 401:
            raise AirtableError("Invalid API key. Check your AIRTABLE_API_KEY.")
        if response.status_code == 403:
            raise AirtableError("Permission denied. Your API key lacks access to this resource.")
        if response.status_code == 404:
            raise AirtableError("Not found. Check that the base/table/record ID is correct.")
        if response.status_code == 422:
            error = response.json().get("error", {})
            raise AirtableError(f"Invalid request: {error.get('message', 'Unknown error')}")
        if response.status_code == 429:
            raise AirtableError("Rate limited. Airtable allows 5 requests/second. Wait and retry.")
        if not response.is_success:
            raise AirtableError(f"Airtable API error: {response.status_code} - {response.text}")

    async def list_bases(self) -> list[dict]:
        """List all bases accessible to the API key.

        Returns:
            List of bases with id, name, permissionLevel
        """
        client = await self._get_client()
        response = await client.get("/meta/bases")
        self._handle_error(response)
        return response.json().get("bases", [])

    async def list_tables(self, base_id: str) -> list[dict]:
        """List all tables in a base.

        Args:
            base_id: The base ID (starts with 'app')

        Returns:
            List of tables with id, name, fields
        """
        client = await self._get_client()
        response = await client.get(f"/meta/bases/{base_id}/tables")
        self._handle_error(response)
        return response.json().get("tables", [])

    async def list_records(
        self,
        base_id: str,
        table_id_or_name: str,
        max_records: int | None = None,
        filter_formula: str | None = None,
    ) -> list[dict]:
        """List records from a table.

        Args:
            base_id: The base ID (starts with 'app')
            table_id_or_name: Table ID or name
            max_records: Maximum records to return (default 100)
            filter_formula: Airtable formula to filter records

        Returns:
            List of records with id, createdTime, fields
        """
        client = await self._get_client()
        params = {}
        if max_records is not None:
            params["maxRecords"] = max_records
        if filter_formula is not None:
            params["filterByFormula"] = filter_formula

        response = await client.get(f"/{base_id}/{table_id_or_name}", params=params)
        self._handle_error(response)
        return response.json().get("records", [])

    async def create_record(
        self,
        base_id: str,
        table_id_or_name: str,
        fields: dict,
    ) -> dict:
        """Create a new record in a table.

        Args:
            base_id: The base ID (starts with 'app')
            table_id_or_name: Table ID or name
            fields: Dictionary of field names to values

        Returns:
            The created record with id, createdTime, fields
        """
        client = await self._get_client()
        payload = {"records": [{"fields": fields}]}
        response = await client.post(f"/{base_id}/{table_id_or_name}", json=payload)
        self._handle_error(response)
        return response.json()["records"][0]

    async def update_record(
        self,
        base_id: str,
        table_id_or_name: str,
        record_id: str,
        fields: dict,
    ) -> dict:
        """Update an existing record.

        Args:
            base_id: The base ID (starts with 'app')
            table_id_or_name: Table ID or name
            record_id: The record ID to update (starts with 'rec')
            fields: Dictionary of field names to new values

        Returns:
            The updated record
        """
        client = await self._get_client()
        payload = {"fields": fields}
        response = await client.patch(
            f"/{base_id}/{table_id_or_name}/{record_id}",
            json=payload
        )
        self._handle_error(response)
        return response.json()
