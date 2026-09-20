const collator = new Intl.Collator("pt-PT", { numeric: true, sensitivity: "base" });

export function compareValues(a: string, b: string, type: string, ascending: boolean): number {
	// Unavailable values stay last in both directions.
	if (a === "" || b === "") return a === b ? 0 : a === "" ? 1 : -1;
	const difference = type === "number" || type === "percentage"
		? Number(a) - Number(b)
		: collator.compare(a, b); // Dates use ISO YYYY-MM-DD keys.
	return ascending ? difference : -difference;
}

export function initSortableTables(root: Document = document): void {
	root.querySelectorAll<HTMLTableElement>("table.sortable").forEach((table) => {
		const tbody = table.tBodies[0];
		if (!tbody) return;
		const headers = table.querySelectorAll<HTMLTableCellElement>("thead th[data-sort]");
		headers.forEach((header) => {
			if (header.querySelector("button")) return;
			const button = document.createElement("button");
			button.type = "button";
			button.className = "sort-button";
			button.append(...header.childNodes);
			const indicator = document.createElement("span");
			indicator.className = "sort-indicator";
			indicator.setAttribute("aria-hidden", "true");
			indicator.textContent = " ↕";
			button.append(indicator);
			header.append(button);
			header.scope = "col";
			button.addEventListener("click", () => {
				const ascending = header.getAttribute("aria-sort") !== "ascending";
				headers.forEach((other) => {
					other.removeAttribute("aria-sort");
					other.querySelector(".sort-indicator")!.textContent = " ↕";
				});
				header.setAttribute("aria-sort", ascending ? "ascending" : "descending");
				indicator.textContent = ascending ? " ↑" : " ↓";
				const value = (row: HTMLTableRowElement) => {
					const cell = row.cells[header.cellIndex];
					return cell?.dataset.sortValue ?? cell?.textContent?.trim() ?? "";
				};
				const rows = Array.from(tbody.rows);
				rows.sort((a, b) => compareValues(value(a), value(b), header.dataset.sort!, ascending));
				tbody.append(...rows);
			});
		});
	});
}
