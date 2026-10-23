"""OpenContext (`opencontext setup hermes`): OpenContext running before every model request."""

import subprocess

COMMAND = __COMMAND__


def _start(**_):
    subprocess.run(COMMAND, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, timeout=30, check=False)


def register(ctx):
    ctx.register_hook("pre_api_request", _start)
