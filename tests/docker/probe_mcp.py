"""A minimal MCP server over stdio for tests/docker/features.py: instructions naming a codename, one
tool returning a word. No dependencies (newline-delimited JSON-RPC)."""

import json
import sys

INSTRUCTIONS = "The probe server's codename is MERCURY."
TOOL = {"name": "probe_word", "description": "Returns the probe server's word.",
        "inputSchema": {"type": "object", "properties": {}}}


def answer(request: dict) -> dict | None:
    method, rid = request.get("method"), request.get("id")
    if rid is None:
        return None  # a notification
    if method == "initialize":
        version = request.get("params", {}).get("protocolVersion", "2025-06-18")
        result = {"protocolVersion": version, "capabilities": {"tools": {}},
                  "serverInfo": {"name": "probe", "version": "1.0"}, "instructions": INSTRUCTIONS}
    elif method == "tools/list":
        result = {"tools": [TOOL]}
    elif method == "tools/call":
        result = {"content": [{"type": "text", "text": "OBSIDIAN"}]}
    elif method in ("resources/list", "prompts/list", "resources/templates/list"):
        result = {method.split("/")[0] if "templates" not in method else "resourceTemplates": []}
    elif method == "ping":
        result = {}
    else:
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"no method {method}"}}
    return {"jsonrpc": "2.0", "id": rid, "result": result}


for line in sys.stdin:
    if line.strip():
        reply = answer(json.loads(line))
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()
