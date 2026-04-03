# Amplicode — Quick Reference

All lookups use the same script pattern.

Each skill contains `scripts/amplicode.py` relative to its own SKILL.md.
Resolve the absolute path to that script before running, then execute:

```bash
MCP_URL="http://127.0.0.1:64442/stream" <absolute-path-to-skill>/scripts/amplicode.py <tool_name> <param>=<value> ...
```

---

## Common calls

Resolve the absolute path to each skill's script before running. The script is at
`scripts/amplicode.py` relative to each skill's SKILL.md.

```bash
# List all domain entities (optionally filter by regex)
# script: <jpa-entity-rules-skill-dir>/scripts/amplicode.py
MCP_URL="http://127.0.0.1:64442/stream" <absolute-path-to-jpa-entity-rules>/scripts/amplicode.py \
    list_all_domain_entities projectPath=$(pwd)

MCP_URL="http://127.0.0.1:64442/stream" <absolute-path-to-jpa-entity-rules>/scripts/amplicode.py \
    list_all_domain_entities projectPath=$(pwd) regexPattern=Bond

# Get details of a specific entity (fields, relationships, parent class)
# script: <jpa-entity-rules-skill-dir>/scripts/amplicode.py
MCP_URL="http://127.0.0.1:64442/stream" <absolute-path-to-jpa-entity-rules>/scripts/amplicode.py \
    get_entity_details projectPath=$(pwd) \
    entityFqn=ru.udya.finapp.investment.instrument.model.Bond
```