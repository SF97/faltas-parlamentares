import meta from "../data/meta.json";

const timestamps = meta as typeof meta & { checked_at?: string; updated_at?: string };

export const DATA_CHECKED_AT = timestamps.checked_at;
export const DATA_UPDATED_AT = timestamps.updated_at;

const PT = new Intl.DateTimeFormat("pt-PT", { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Lisbon" });

export function formatPT(value: string | undefined): string {
	const d = value ? new Date(value) : null;
	if (!d || Number.isNaN(d.getTime())) return "não registada";
	return PT.format(d);
}
