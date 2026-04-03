#!/usr/bin/env python3
"""
Universal Amplicode MCP client.

Usage:
    amplicode_mcp.py <tool_name> [key=value ...]

    Values are parsed as JSON when possible, otherwise treated as strings.
    Array values must be passed as JSON: files='["a.java","b.java"]'

Examples:
    amplicode_mcp.py get_project_summary projectPath=/my/project
    amplicode_mcp.py list_project_endpoints projectPath=/my/project
    amplicode_mcp.py get_endpoint_info projectPath=/my/project httpMethod=POST fullUrl=/rest/investment/structured/{id}/optimize-quantity
    amplicode_mcp.py list_all_domain_entities projectPath=/my/project regexPattern=Bond
    amplicode_mcp.py analyze_files projectPath=/my/project files='["src/main/java/Foo.java"]'
    amplicode_mcp.py rebuild_project projectPath=/my/project rebuild=true
    amplicode_mcp.py run_tests projectPath=/my/project onlyFailed=true
    amplicode_mcp.py --list

Special flags:
    --list      List all available MCP tools with their parameters and exit.
    --raw       Print raw JSON response instead of pretty-printed output.

Required env var:
    MCP_URL — Streamable HTTP URL of the Amplicode MCP server
              e.g. export MCP_URL="http://127.0.0.1:64442/stream"
"""

import json
import os
import sys
import urllib.request
from typing import Any, Dict, Optional, Tuple

# ── env / args ─────────────────────────────────────────────────────────────────

MCP_URL = os.environ.get("MCP_URL")
if not MCP_URL:
    print("ERROR: MCP_URL environment variable is not set", file=sys.stderr)
    print('  export MCP_URL="http://127.0.0.1:64442/stream"', file=sys.stderr)
    sys.exit(1)

MCP_TIMEOUT = float(os.environ.get("MCP_TIMEOUT", "5"))

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(0)

# Parse flags and positional args
args = sys.argv[1:]
FLAG_LIST = "--list" in args
FLAG_RAW  = "--raw"  in args
args = [a for a in args if a not in ("--list", "--raw")]

TOOL_NAME = args[0] if args else None


def parse_kwargs(raw_args: list[str]) -> Dict[str, Any]:
    """Parse key=value pairs; values are decoded as JSON when possible."""
    result: Dict[str, Any] = {}
    for token in raw_args:
        if "=" not in token:
            print(f"WARNING: skipping argument without '=': {token!r}", file=sys.stderr)
            continue
        k, _, v = token.partition("=")
        try:
            result[k] = json.loads(v)
        except json.JSONDecodeError:
            result[k] = v
    return result


# ── MCP transport ──────────────────────────────────────────────────────────────

def mcp_request(payload: Dict, session_id: Optional[str] = None) -> Tuple[Dict, Dict]:
    """Send a JSON-RPC 2.0 request. Returns (body, response_headers)."""
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        MCP_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            **({"mcp-session-id": session_id} if session_id else {}),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=MCP_TIMEOUT) as resp:
        headers = dict(resp.headers)
        body = json.loads(resp.read().decode())
    return body, headers


def mcp_init() -> str:
    """Initialize MCP session and return session ID."""
    _, headers = mcp_request({
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "amplicode-mcp-cli", "version": "1.0"},
        },
    })
    sid = headers.get("mcp-session-id") or headers.get("Mcp-Session-Id")
    if not sid:
        print("ERROR: Failed to obtain mcp-session-id", file=sys.stderr)
        print(f"Response headers: {headers}", file=sys.stderr)
        sys.exit(1)
    return sid


def mcp_tools_list(session_id: str) -> list:
    """Return the list of available MCP tools."""
    body, _ = mcp_request(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        session_id=session_id,
    )
    return body.get("result", {}).get("tools", [])


def mcp_call(session_id: str, tool_name: str, arguments: Dict) -> Any:
    """Call an MCP tool and return the structured result."""
    body, _ = mcp_request(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        },
        session_id=session_id,
    )
    error = body.get("error")
    if error:
        print(f"ERROR from MCP: {json.dumps(error, ensure_ascii=False, indent=2)}", file=sys.stderr)
        sys.exit(1)

    result = body.get("result", {})
    data = result.get("structuredContent")
    if data is None:
        content = result.get("content") or [{}]
        text = content[0].get("text", "null")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = text
    return data


# ── helpers ────────────────────────────────────────────────────────────────────

def print_tools(tools: list) -> None:
    """Pretty-print available tools and their parameters."""
    print(f"\nAvailable Amplicode MCP tools ({len(tools)} total):\n")
    for tool in tools:
        name = tool["name"]
        desc = tool.get("description", "").split("\n")[0][:100]
        schema = tool.get("inputSchema", {})
        props = schema.get("properties", {})
        required = set(schema.get("required", []))

        print(f"  {name}")
        if desc:
            print(f"    {desc}")
        for k, v in props.items():
            req_mark = " [required]" if k in required else ""
            type_str = v.get("type", "?")
            param_desc = v.get("description", "").replace("\n", " ")[:60]
            print(f"    • {k}: {type_str}{req_mark}  {param_desc}")
        print()


# ── main ───────────────────────────────────────────────────────────────────────

print(f"Connecting to MCP: {MCP_URL}", file=sys.stderr)
session_id = mcp_init()
print(f"Session: {session_id}", file=sys.stderr)

if FLAG_LIST or TOOL_NAME is None:
    tools = mcp_tools_list(session_id)
    print_tools(tools)
    sys.exit(0)

# Parse remaining key=value arguments
kwargs = parse_kwargs(args[1:])

print(f"Tool      : {TOOL_NAME}", file=sys.stderr)
print(f"Arguments : {json.dumps(kwargs, ensure_ascii=False)}", file=sys.stderr)
print(file=sys.stderr)

result = mcp_call(session_id, TOOL_NAME, kwargs)

if FLAG_RAW or not isinstance(result, (dict, list)):
    print(json.dumps(result, ensure_ascii=False, indent=2))
else:
    print(json.dumps(result, ensure_ascii=False, indent=2))