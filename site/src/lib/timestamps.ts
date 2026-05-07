import { execSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = resolve(dirname(fileURLToPath(import.meta.url)), "../../..");

function lastDataChangeISO(): string {
	try {
		const out = execSync("git log -1 --format=%cI -- site/src/data", {
			cwd: repoDir,
			encoding: "utf8",
			stdio: ["ignore", "pipe", "ignore"],
		}).trim();
		if (out) return out;
	} catch {
		// fall through
	}
	return new Date().toISOString();
}

export const BUILD_TIME = new Date();
export const DATA_UPDATED_AT = new Date(lastDataChangeISO());

const PT = new Intl.DateTimeFormat("pt-PT", { day: "numeric", month: "long", year: "numeric" });

export function formatPT(d: Date): string {
	return PT.format(d);
}
