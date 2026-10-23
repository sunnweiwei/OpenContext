import os
import tempfile

# Every test in an OpenContext directory of its own: nothing a test runs writes to the user's
# (~/.config/opencontext: the harnesses installed, the conversations noted).
os.environ.setdefault("OPENCONTEXT_HOME", tempfile.mkdtemp(prefix="opencontext-tests-"))
