// OpenContext (`opencontext setup pi`): OpenContext running before every agent run. `opencontext uninstall pi` removes this file.
import { execSync } from "node:child_process";

const COMMAND = __COMMAND__;

export default function (pi: any) {
  pi.on("before_agent_start", async () => {
    try {
      execSync(COMMAND, { stdio: "ignore", shell: "/bin/sh", timeout: 30000 });
    } catch {}
  });
}
