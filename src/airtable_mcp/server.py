"""MCP server for Airtable integration."""

from mcp.server.fastmcp import FastMCP
from airtable_mcp.client import AirtableClient, AirtableError

# Initialize the MCP server
mcp = FastMCP("airtable")

# Lazy-initialized client
_client: AirtableClient | None = None


def get_client() -> AirtableClient:
    """Get or create the Airtable client."""
    global _client
    if _client is None:
        _client = AirtableClient()
    return _client


@mcp.tool()
async def list_bases() -> list[dict]:
    """List all Airtable bases accessible to your account.

    Returns a list of bases with their ID, name, and your permission level.
    Use the base ID in subsequent calls to list_tables and record operations.
    """
    return await get_client().list_bases()


@mcp.tool()
async def list_tables(base_id: str) -> list[dict]:
    """List all tables in an Airtable base.

    Args:
        base_id: The base ID (starts with 'app', e.g., 'appABC123')

    Returns a list of tables with their ID, name, and field definitions.
    Use the table ID or name in record operations.
    """
    return await get_client().list_tables(base_id)


@mcp.tool()
async def list_records(
    base_id: str,
    table_id_or_name: str,
    max_records: int = 100,
    filter_formula: str | None = None,
) -> list[dict]:
    """List records from an Airtable table.

    Args:
        base_id: The base ID (starts with 'app')
        table_id_or_name: Table ID (starts with 'tbl') or table name
        max_records: Maximum number of records to return (default 100)
        filter_formula: Airtable formula to filter records, e.g., "{Status}='Done'"

    Returns a list of records with their ID, creation time, and field values.
    """
    return await get_client().list_records(
        base_id,
        table_id_or_name,
        max_records=max_records,
        filter_formula=filter_formula,
    )


@mcp.tool()
async def create_record(
    base_id: str,
    table_id_or_name: str,
    fields: dict,
) -> dict:
    """Create a new record in an Airtable table.

    Args:
        base_id: The base ID (starts with 'app')
        table_id_or_name: Table ID or table name
        fields: Dictionary mapping field names to values

    Returns the created record with its new ID and all field values.

    Example:
        create_record("appABC123", "Tasks", {"Name": "New Task", "Status": "Pending"})
    """
    return await get_client().create_record(base_id, table_id_or_name, fields)


@mcp.tool()
async def update_record(
    base_id: str,
    table_id_or_name: str,
    record_id: str,
    fields: dict,
) -> dict:
    """Update an existing record in an Airtable table.

    Args:
        base_id: The base ID (starts with 'app')
        table_id_or_name: Table ID or table name
        record_id: The record ID to update (starts with 'rec')
        fields: Dictionary of field names to new values (only specified fields are updated)

    Returns the updated record with all field values.

    Example:
        update_record("appABC123", "Tasks", "recXYZ789", {"Status": "Done"})
    """
    return await get_client().update_record(base_id, table_id_or_name, record_id, fields)


def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
