# Amplicode MCP — Quick Reference

All MCP lookups use the same script pattern:

```bash
MCP_URL="http://127.0.0.1:64442/stream" python3 .claude/skills/<skill-name>/scripts/amplicode_mcp.py <tool_name> <param>=<value> ...
```

Prefer using the named skill (e.g. `list-endpoints`) over calling the script directly — skills may include additional post-processing. Fall back to the script only if the skill is unavailable.

---

## Common calls

```bash
# List all endpoints
MCP_URL="http://127.0.0.1:64442/stream" python3 .claude/skills/list-endpoints/scripts/amplicode_mcp.py \
    list_project_endpoints projectPath=/Users/ikuchmin/Documents/Financial/finapp

# Get details of a specific endpoint (returnType, params, FQN)
MCP_URL="http://127.0.0.1:64442/stream" python3 .claude/skills/get-endpoint-info/scripts/amplicode_mcp.py \
    get_endpoint_info projectPath=/Users/ikuchmin/Documents/Financial/finapp \
    methodFqn=ru.udya.finapp.investment.instrument.controller.BondController#getAll

# Get entity fields and relationships
MCP_URL="http://127.0.0.1:64442/stream" python3 .claude/skills/get-entity-details/scripts/amplicode_mcp.py \
    get_entity_details projectPath=/Users/ikuchmin/Documents/Financial/finapp \
    entityFqn=ru.udya.finapp.investment.instrument.model.Bond

# List repositories for an entity
MCP_URL="http://127.0.0.1:64442/stream" python3 .claude/skills/list-entity-repositories/scripts/amplicode_mcp.py \
    list_entity_repositories projectPath=/Users/ikuchmin/Documents/Financial/finapp

# List mappers for an entity
MCP_URL="http://127.0.0.1:64442/stream" python3 .claude/skills/list-entity-mappers/scripts/amplicode_mcp.py \
    list_entity_mappers projectPath=/Users/ikuchmin/Documents/Financial/finapp
```