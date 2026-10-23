// OpenContext (`opencontext setup`): OpenContext running before every model request. `opencontext uninstall` removes this file.
import { execSync } from "node:child_process";

const COMMAND = __COMMAND__;

export const OpenContextStart = async () => ({
  "chat.params": async () => {
    try {
      execSync(COMMAND, { stdio: "ignore", shell: "/bin/sh", timeout: 30000 });
    } catch {}
  },
});
