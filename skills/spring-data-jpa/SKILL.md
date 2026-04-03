---
name: spring-data-jpa
description: Rules and guidelines for working with Spring Data JPA in the project. ALWAYS use this skill when adding, removing, or modifying JPA entities, repositories, or projections. Trigger on any request that involves changing entity structure, adding new entities, modifying field annotations, updating database mappings, creating or modifying Spring Data repositories, or defining query projections (interfaces, DTOs).
---

# Working with JPA Entities

When the task involves creating or modifying a JPA entity:

1. If entity conventions have not been detected yet in this conversation — check memory for previously saved conventions first. If found in memory, reuse them. Otherwise read `references/entity-conventions.md` and follow all substeps there to detect project conventions.
2. Read `references/entity-rules-impl.md` and follow the rules there when writing or modifying the entity

# Working with Transactions

When the task involves adding or modifying transactional behavior:

1. If transaction conventions have not been detected yet in this conversation — check memory for previously saved conventions first. If found in memory, reuse them. Otherwise read `references/transaction-conventions.md` and follow all substeps there to detect project conventions.
2. Read `references/transaction-rules-impl.md` and follow the rules there when writing or modifying transactional code.

---

## Amplicode MCP Tools

See `references/amplicode-mcp-calls.md` to understand how to call available tools via `amplicode.py`.

The `projectPath` is always the root of the current project. Use `get_entity_details` to check parent class before adding `id`, and to inspect existing fields before adding new ones.
