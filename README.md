# Airtable MCP Server

A Model Context Protocol (MCP) server that lets Claude Desktop interact with your Airtable bases. List bases, browse tables, and create/update records through natural conversation.

## Features

- **list_bases** - See all your Airtable bases
- **list_tables** - View tables and their fields in a base
- **list_records** - Query records with optional filtering
- **create_record** - Add new records to any table
- **update_record** - Modify existing records

## Setup

### 1. Get Your Airtable API Key

1. Go to [airtable.com/create/tokens](https://airtable.com/create/tokens)
2. Create a new personal access token
3. Add scopes: `data.records:read`, `data.records:write`, `schema.bases:read`
4. Add access to the bases you want to use
5. Copy the token (starts with `pat`)

### 2. Configure Claude Desktop

Add this to your Claude Desktop config file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "airtable": {
      "command": "uv",
      "args": ["run", "--directory", "C:\\path\\to\\airtable-mcp-server", "airtable-mcp"],
      "env": {
        "AIRTABLE_API_KEY": "pat_your_token_here"
      }
    }
  }
}
```

Replace:
- `C:\\path\\to\\airtable-mcp-server` with the actual path to this folder
- `pat_your_token_here` with your Airtable personal access token

### 3. Restart Claude Desktop

Close and reopen Claude Desktop to load the new MCP server.

## Usage Examples

Once configured, you can ask Claude things like:

- "List my Airtable bases"
- "What tables are in my Project Tracker base?"
- "Show me all records in the Tasks table"
- "Create a new task called 'Review proposal' with status 'Pending'"
- "Mark task recXYZ as Done"
- "Find all tasks where Status is 'In Progress'"

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Airtable account with API access

## Development

```bash
# Install dependencies
uv sync

# Run the server directly (for testing)
uv run airtable-mcp
```

## License

MIT
