#!/bin/sh
# Install OpenContext and its `opencontext` command:
#
#   curl -fsSL https://raw.githubusercontent.com/sunnweiwei/OpenContext/main/install.sh | sh
#   sh install.sh [SOURCE]      # SOURCE: a checkout, a wheel or a pip URL (default: the GitHub repository)
#
# OpenContext gets an environment of its own (uv's tool environment where uv is installed, else a
# virtual environment in ~/.local/share/opencontext), and `opencontext` goes in ~/.local/bin. Running it again
# upgrades OpenContext. Then: `opencontext setup <harness> --strategy <name>` (`opencontext help` is the guide).
set -eu

SOURCE="${1:-git+https://github.com/sunnweiwei/OpenContext.git}"
BIN="$HOME/.local/bin"
mkdir -p "$BIN"

if command -v uv >/dev/null 2>&1; then
  uv tool install --quiet --force --reinstall "$SOURCE"
  OPENCONTEXT="$(uv tool dir --bin 2>/dev/null || echo "$BIN")/opencontext"
else
  PYTHON="$(command -v python3 || command -v python || true)"
  if [ -z "$PYTHON" ] || ! "$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
    echo "opencontext: needs Python 3.11 or newer (or uv: https://docs.astral.sh/uv/)" >&2
    exit 1
  fi
  VENV="$HOME/.local/share/opencontext/venv"
  if [ ! -x "$VENV/bin/python" ] && ! "$PYTHON" -m venv "$VENV" >/dev/null 2>&1; then
    rm -rf "$VENV"
    echo "opencontext: Python cannot make a virtual environment here (on Debian or Ubuntu: apt install python3-venv)," >&2
    echo "       or install uv (https://docs.astral.sh/uv/) and run this again" >&2
    exit 1
  fi
  "$VENV/bin/python" -m pip install --quiet --disable-pip-version-check --upgrade "$SOURCE"
  ln -sf "$VENV/bin/opencontext" "$BIN/opencontext"
  OPENCONTEXT="$BIN/opencontext"
fi

echo "OpenContext installed: $OPENCONTEXT"
FOLDER="$(dirname "$OPENCONTEXT")"
case ":$PATH:" in
  *":$FOLDER:"*) ;;
  *)  # as uv's and rustup's installers do: the folder on PATH for shells started from now on
    LINE="export PATH=\"$FOLDER:\$PATH\"  # added by OpenContext's installer"
    for RC in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.zshrc"; do
      case "$RC" in
        */.profile) ;;
        */.bashrc) [ -f "$RC" ] || [ "$(basename "${SHELL:-}")" = bash ] || continue ;;
        */.zshrc) [ -f "$RC" ] || [ "$(basename "${SHELL:-}")" = zsh ] || continue ;;
      esac
      grep -qsF "added by OpenContext's installer" "$RC" || echo "$LINE" >> "$RC"
    done
    echo "  note: $FOLDER is now on PATH for new shells; in this one, run OpenContext as $OPENCONTEXT"
    ;;
esac
echo "Next: opencontext setup <harness> --strategy <name>   (opencontext help: the guide)"
