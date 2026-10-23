# Image for testing real harnesses through OpenContext. Built once; the repo, Codex and
# Claude Code binaries, credentials and a throwaway HOME are mounted at run time.
FROM node:24-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip ripgrep \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --break-system-packages --no-cache-dir httpx starlette uvicorn
RUN npm install -g --no-fund --no-audit \
    @earendil-works/pi-coding-agent opencode-ai @google/gemini-cli \
    @charmland/crush @kilocode/cli openclaw
RUN pip3 install --break-system-packages --no-cache-dir zstandard
RUN curl -fsSL https://github.com/block/goose/releases/download/stable/download_cli.sh \
    | GOOSE_BIN_DIR=/usr/local/bin CONFIGURE=false bash
RUN curl -fsSL https://code.kimi.com/kimi-code/install.sh \
    | KIMI_INSTALL_DIR=/opt/kimi-code KIMI_NO_MODIFY_PATH=1 bash \
    && ln -sf /opt/kimi-code/bin/kimi /usr/local/bin/kimi && chmod -R a+rX /opt/kimi-code
RUN npm install -g --no-fund --no-audit @deepseek-ai/dsh
RUN npm install -g --no-fund --no-audit @tencent-ai/codebuddy-code
RUN pip3 install --break-system-packages --no-cache-dir nanobot-ai hermes-agent mini-swe-agent
# OPENCONTEXT_STRATEGY=rlm runs the RLM authors' package inside OpenContext.
RUN pip3 install --break-system-packages --no-cache-dir rlms==0.1.3
# LiteLLM's proxy in a venv of its own: it needs mcp>=2.2, nanobot needs mcp<2. Last, so
# that mini-swe-agent's own litellm (a library) does not take over the command.
RUN apt-get update && apt-get install -y --no-install-recommends python3-venv && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/litellm && /opt/litellm/bin/pip install --no-cache-dir 'litellm[proxy]' \
    && ln -sf /opt/litellm/bin/litellm /usr/local/bin/litellm
