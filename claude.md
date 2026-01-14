# Airtable MCP Server

## Goal
Build a standalone MCP server for Airtable that works with Claude Desktop via **one-click .mcpb extension install**. This is a proposal deliverable for an Upwork job - needs to be clean, working, and demonstrable in a 2-min Loom.

## Status: PIVOTED TO EXTENSION
Originally planned as a Python MCP server with manual JSON config. **Pivoted to Node.js .mcpb extension** for one-click install (much better demo).

**Active repo:** https://github.com/ldraney/airtable-mcpb
**Issue tracking work:** https://github.com/ldraney/airtable-mcpb/issues/1

## Why Extension (.mcpb) Over Manual Config
- Manual JSON config = friction = bad demo
- .mcpb extension = drag-and-drop install = great demo
- API key prompt on install (no env var editing!)
- "One-click install" is the selling point

## Tech Stack (Extension)
- Node.js + `@modelcontextprotocol/sdk`
- `zod` for input schemas
- `mcpb` CLI for packaging
- stdio transport

## Tools Implemented
1. `list_bases` - List all accessible bases
2. `list_tables` - List tables in a base
3. `list_records` - Get records (with optional max_records)
4. `create_record` - Create record (fields_json as JSON string)
5. `update_record` - Update record (fields_json as JSON string)

## Key Technical Learnings
- Empty inputSchema `{}` breaks zod - use placeholder field
- `z.record(z.any())` doesn't work - use JSON string instead
- Version bump in manifest.json forces fresh install
- Node.js extensions work better than Python (dependency bundling)

## Airtable API Key Scopes Needed
- `data.records:read`
- `data.records:write`
- `schema.bases:read`

## Files Structure (airtable-mcpb repo)
```
airtable-mcpb/
├── manifest.json          # Extension metadata, user_config for API key
├── package.json           # Node.js deps
├── server/
│   └── index.js           # MCP server with 5 tools
├── airtable-mcpb.mcpb     # Built extension (installable)
└── HANDOFF.md             # Session notes
```

## Commands
```bash
# Repack after code changes
cd C:\Users\drane\airtable-mcpb && mcpb pack

# Check extension logs
tail -50 "%APPDATA%\Claude\logs\mcp-server-airtable.log"

# Install in Claude Desktop
# Settings → Extensions → Install Extension → select .mcpb file
```

## User Story
**As a** Claude Desktop user with Airtable data,
**I want** to install an Airtable extension with one click,
**So that** I can query and modify my Airtable bases through natural conversation.

## Acceptance Criteria
- [ ] Extension installs via drag-drop .mcpb (no CLI, no JSON editing)
- [ ] User is prompted for API key during install (not env vars)
- [ ] `list_bases` returns user's actual Airtable bases
- [ ] `list_tables` returns tables for a given base
- [ ] `list_records` returns records from a table
- [ ] `create_record` creates a record visible in Airtable UI
- [ ] `update_record` modifies a record visible in Airtable UI
- [ ] Errors are user-friendly (not stack traces)
- [ ] 2-min Loom demo shows full flow

## What's Left
- [ ] Test create_record and update_record with real data
- [ ] Test error handling (bad API key)
- [ ] Record Loom demo
- [ ] Submit Upwork proposal

## Loom Demo Script (60-90 sec)

**Opening (5 sec):**
> "Here's a standalone Airtable MCP server - one-click install, no JSON config editing. API key is prompted during setup. Let me show you it working..."

**1. Install (10 sec)**
- Drag .mcpb into Claude Desktop
- Show API key prompt
- Extension enabled

**2. Auth Works (10 sec)**
- "List my Airtable bases"
- Show actual bases appear

**3. CRUD Operations (30-45 sec)**
- "What tables are in [base]?" → tables appear
- "Create a record in [table] with Name='Demo' and Status='Active'"
- Switch to Airtable UI → show record exists

**4. Error Handling (optional, 10 sec)**
- Show graceful error message for bad API key

**Closing:**
> "Clean standalone server. No Pipedream dependency. Ready to build more integrations like this."

## Proposal Text (Draft)
```
I built a working Airtable MCP server as a proof of concept:

✅ One-click install (.mcpb extension format)
✅ API key prompted during setup (no manual config editing)
✅ All CRUD operations: list bases, tables, records + create/update
✅ Clean error handling

Video demo attached showing it working in Claude Desktop.

I can build similar standalone MCP servers for other Pipedream integrations.
Timeline depends on API complexity - simple auth like Airtable is fast,
OAuth flows need more work.

Happy to discuss scope and priorities.
```
