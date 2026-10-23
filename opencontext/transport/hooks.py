"""OpenContext's endpoint for harness hooks: a harness compacting its own history asks OpenContext's
strategy what the history should become (`opencontext.integrations`)."""

from __future__ import annotations

import logging

from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from ..core.engine import Engine
from ..integrations import HOOKS

log = logging.getLogger("opencontext")


def hook_routes(engine: Engine) -> list[Route]:
    async def compact(request: Request) -> Response:
        try:
            payload = await request.json()
            hook = HOOKS[payload.get("harness")]
            return JSONResponse(await run_in_threadpool(hook.compact, engine, payload))
        except Exception as error:  # the harness then compacts as it would without OpenContext
            log.warning("hook compaction failed", exc_info=True)
            return JSONResponse({"error": {"message": f"opencontext: {error!r:.300}"}}, 500)

    return [Route("/opencontext/v1/compact", compact, methods=["POST"])]
