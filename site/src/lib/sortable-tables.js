// Torna as tabelas ordenáveis ao clicar nos cabeçalhos.
// Melhoria progressiva: sem JS, as tabelas mantêm a ordem gerada no build.
//
// Convenções:
// - `<th class="num">` ordena numericamente; as restantes colunas ordenam por texto (pt-PT).
// - `<td data-sort="...">` sobrepõe-se ao texto da célula como valor de ordenação.
// - `<table data-sortable="false">` fica de fora.

const collator = new Intl.Collator("pt-PT", { numeric: true, sensitivity: "base" });

const cellValue = (row, index) => {
	const cell = row.cells[index];
	if (!cell) return "";
	const override = cell.getAttribute("data-sort");
	return override !== null ? override : (cell.textContent || "").trim();
};

const toNumber = (value) => {
	const n = Number.parseFloat(value.replace(/\s/g, "").replace(",", "."));
	return Number.isNaN(n) ? null : n;
};

const compareNumeric = (a, b, direction) => {
	const na = toNumber(a);
	const nb = toNumber(b);
	// Células sem número (vazias, "—") ficam sempre no fim, nas duas direções.
	if (na === null && nb === null) return 0;
	if (na === null) return 1;
	if (nb === null) return -1;
	return direction === "asc" ? na - nb : nb - na;
};

const sortBy = (table, index, direction) => {
	const tbody = table.tBodies[0];
	const headers = Array.from(table.tHead.rows[0].cells);
	const numeric = headers[index].classList.contains("num");
	const rows = Array.from(tbody.rows);

	// Array.prototype.sort é estável: em caso de empate, as linhas mantêm a ordem
	// com que vieram do build (que já é a ordenação útil por omissão).
	rows.sort((a, b) => {
		const va = cellValue(a, index);
		const vb = cellValue(b, index);
		if (numeric) return compareNumeric(va, vb, direction);
		const c = collator.compare(va, vb);
		return direction === "asc" ? c : -c;
	});

	// appendChild move as linhas existentes: estilos inline (p. ex. filtros) e
	// listeners são preservados.
	const frag = document.createDocumentFragment();
	for (const row of rows) frag.appendChild(row);
	tbody.appendChild(frag);

	headers.forEach((th, i) => {
		if (i === index) th.setAttribute("aria-sort", direction === "asc" ? "ascending" : "descending");
		else th.removeAttribute("aria-sort");
	});
};

const enhance = (table) => {
	if (table.dataset.sortable === "false") return;
	if (!table.tHead || !table.tHead.rows.length || !table.tBodies.length) return;
	if (table.tBodies[0].rows.length < 2) return;

	const headers = Array.from(table.tHead.rows[0].cells);

	headers.forEach((th, index) => {
		if (th.dataset.sortable === "false") return;

		// O conteúdo do cabeçalho passa para dentro de um botão, para o ordenar
		// também funcionar por teclado.
		const btn = document.createElement("button");
		btn.type = "button";
		btn.className = "sort-btn";
		while (th.firstChild) btn.appendChild(th.firstChild);

		const arrow = document.createElement("span");
		arrow.className = "sort-arrow";
		arrow.setAttribute("aria-hidden", "true");
		btn.appendChild(arrow);

		th.appendChild(btn);
		th.classList.add("sortable");

		btn.addEventListener("click", () => {
			const current = th.getAttribute("aria-sort");
			let direction;
			if (current === "ascending") direction = "desc";
			else if (current === "descending") direction = "asc";
			// Primeiro clique: contagens começam na maior (mais útil num ranking),
			// texto começa em A→Z.
			else direction = th.classList.contains("num") ? "desc" : "asc";
			sortBy(table, index, direction);
		});
	});
};

document.querySelectorAll("table").forEach(enhance);
