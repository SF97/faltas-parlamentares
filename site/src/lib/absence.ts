/** Each recorded status belongs to exactly one side of the calculation. */
export function absencePercentage(records: Record<string, number>[]): number | null {
	let absences = 0;
	let work = 0;
	for (const totals of records) {
		absences += (totals.FJ ?? 0) + (totals.FI ?? 0) + (totals.F ?? 0);
		work += (totals.P ?? 0) + (totals.AMP ?? 0) + (totals.PNO ?? 0) + (totals.FQV ?? 0);
	}
	const total = absences + work;
	return total === 0 ? null : (100 * absences) / total;
}

const formatter = new Intl.NumberFormat("pt-PT", {
	style: "percent",
	minimumFractionDigits: 1,
	maximumFractionDigits: 1,
});

export const unavailableExplanation = "Sem registos para calcular a percentagem de faltas.";

export function formatAbsencePercentage(value: number | null): string {
	return value === null ? "—" : formatter.format(value / 100);
}
