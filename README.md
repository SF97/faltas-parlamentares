# faltas-parlamentares

Site público, em português europeu, que acompanha as ausências dos deputados da Assembleia da República na XVII Legislatura (em curso).

🔗 **[faltasparlamentares.sergioferreira.net](https://faltasparlamentares.sergioferreira.net)**

[![Quem falta mais ao plenário?](site/public/og.png)](https://faltasparlamentares.sergioferreira.net)

Os dados vêm das páginas oficiais de [presenças em reuniões plenárias](https://www.parlamento.pt/DeputadoGP/Paginas/reunioesplenarias.aspx) publicadas pelo Parlamento (uma por deputado), complementadas pelo [portal de dados abertos](https://www.parlamento.pt/Cidadania/paginas/dadosabertos.aspx) para metadados. Não há comentário editorial nem interpretação política — só os números, organizados de forma legível.

## Estrutura

- `ingest/` — pipeline em Python (3.15, [pnpm](https://pnpm.io), httpx) que faz scraping das páginas "Presenças às Reuniões Plenárias" e escreve JSON para `site/src/data/`.
- `site/` — site estático em [Astro](https://astro.build), gerado a partir dos JSON do `ingest/`.
- `.github/workflows/update.yml` — cron diário (06:00 UTC) que corre o `ingest` e faz commit e push dos dados se mudaram. O push desencadeia o build e a publicação no Cloudflare Pages através da integração com o GitHub.

## Desenvolvimento

Com [mise](https://mise.jdx.dev/), a partir da raiz do repositório:

```bash
mise install --monorepo # instala as ferramentas dos dois projetos
mise //:install        # instala as dependências Python e JavaScript
mise //:lint           # executa todos os linters do repositório
mise //:lint-actions   # verifica GitHub Actions e os scripts shell
mise //ingest:sync    # instala as dependências Python
mise //ingest:run     # corre o ingest com a cache HTTP local
mise //ingest:refresh # corre o ingest sem a cache HTTP
mise //ingest:lint    # verifica e valida a formatação do Python
mise //ingest:lint-fix # corrige e formata o Python
mise //ingest:format  # formata o Python
mise //site:dev       # inicia o site em http://localhost:4321
mise //site:build     # gera site/dist
mise //site:lint      # verifica JavaScript, TypeScript e frontmatter Astro
mise //site:lint-fix  # corrige automaticamente problemas do Oxlint
mise //site:preview   # pré-visualiza o site gerado
```

Os comandos subjacentes também podem ser executados diretamente:

```bash
# Workspace (a partir da raiz)
pnpm install --frozen-lockfile
pnpm dev        # inicia o site
pnpm build      # gera site/dist/
pnpm lint       # executa os linters através do mise (requer mise)
pnpm ingest     # corre o ingest através do mise (requer mise)

# Ingest (Python)
cd ingest
pnpm --dir . exec python -m ingest.main                  # usa cache local em ingest/.cache/http
FALTAS_NO_CACHE=1 pnpm --dir . exec python -m ingest.main  # força re-fetch (como o CI)
pnpm --dir . exec ruff check .
pnpm --dir . exec ruff format --check .

# Site (Astro) — pnpm, não npm
cd ../site
pnpm dev        # http://localhost:4321
pnpm build      # gera dist/
pnpm lint       # verifica JavaScript, TypeScript e frontmatter Astro
pnpm lint:fix   # corrige automaticamente problemas do Oxlint
pnpm preview    # serve dist/
```

As tarefas `mise //ingest:run` e `mise //ingest:refresh` instalam apenas as dependências Python de execução; `mise //ingest:sync` inclui também o Ruff. As tarefas do site instalam apenas as dependências JavaScript desse projeto. `mise //:install` prepara ambos os projetos por completo; o lint agregado instala apenas dependências de desenvolvimento. O `act` e os linters dos workflows são ferramentas das respetivas tarefas mise, instaladas apenas quando utilizadas.

O lint agregado também executa o actionlint a partir da raiz. A tarefa instala o actionlint e o ShellCheck através do mise para validar os blocos `run:` dos workflows.

Para validar os workflows localmente com Docker e `act` num Mac ARM64:

```bash
mise run act -- push -W .github/workflows/lint.yml -P ubuntu-26.04=catthehacker/ubuntu:act-24.04 --container-architecture linux/arm64
mise run act -- workflow_dispatch -W .github/workflows/ingest.yml -P ubuntu-26.04=catthehacker/ubuntu:act-24.04 --container-architecture linux/arm64
```

O runner local usa Ubuntu 24.04; o GitHub Actions usa Ubuntu 26.04. A cache da ação mise fica desativada sob `act`, e o workflow de atualização não faz commit nem push nas execuções locais. Num host x64, usar `linux/amd64`.

Os JSON gerados pelo `ingest` são commitados para o repositório — o site não corre o ingest no build.

Para publicar a partir da raiz, usar `pnpm build` como comando de build e `site/dist` como diretório de saída.

O pnpm 12.15.0 tem configuração e `pnpm-lock.yaml` na raiz. O workspace inclui `site/` e `ingest/`; o pnpm lê o projeto Python a partir de `ingest/pyproject.toml`, sem precisar de `ingest/package.json`. O mise define as tarefas do ingest; os atalhos `pnpm lint` e `pnpm ingest` delegam no mise. Uma instalação na raiz prepara ambos os projetos; o Python mantém o seu `ingest/pylock.toml` e a sua `ingest/.venv`. O `ingest/pylock.toml` inclui Python 3.15 em macOS ARM64, Linux x64 (CI) e Linux ARM64 (act local). Após alterar dependências, executar `pnpm install --no-frozen-lockfile` na raiz e incluir os lockfiles no commit. Numa migração de uv, mover primeiro a antiga `.venv`: o pnpm não substitui ambientes criados por outras ferramentas. O Dependabot acompanha o `pyproject.toml` através do ecossistema `pip`; o lockfile deve ser regenerado nessas atualizações.

O `meta.json` guarda `checked_at` após cada execução bem-sucedida do ingest e `updated_at` quando o conteúdo dos dados muda. Uma execução sem alterações mantém `updated_at`, mas atualiza `checked_at`, originando um commit e uma publicação para mostrar a verificação mais recente. O rodapé apresenta estas datas no fuso horário de Lisboa; datas ainda não registadas aparecem como «não registada». Para verificar os dados diretamente na fonte, sem reutilizar a cache HTTP, usar `mise //ingest:refresh`, como no workflow diário.

O workflow **Update Python lockfile** corre automaticamente nos PRs do Dependabot que alteram `ingest/pyproject.toml`. Regenera o lockfile Python e faz commit apenas de `ingest/pylock.toml` no ramo do PR, usando o token automático do GitHub; não exige secrets adicionais. Após o commit, se os checks aguardarem aprovação, selecionar **Approve workflows to run** no PR. Para repetir manualmente, abrir **Actions → Update Python lockfile → Run workflow** e indicar o número do PR. A opção manual fica disponível depois de o workflow ser integrado no ramo predefinido.

## Classificação das ausências

Cada reunião plenária é classificada pelo Parlamento numa de sete categorias, todas usadas no site:

| Código | Significado |
|--------|-------------|
| **P** | Presença |
| **FJ** | Falta Justificada |
| **FI** | Falta Injustificada |
| **AMP** | Ausência em Missão Parlamentar |
| **FQV** | Falta ao Quórum de Votação |
| **PNO** | Presença Noutro Órgão |
| **F** | Falta (não classificada — provisória, geralmente reclassificada como FJ nas semanas seguintes) |

Ver [`/metodologia`](https://faltasparlamentares.sergioferreira.net/metodologia) no site para detalhes, incluindo o tratamento de substituições temporárias entre efetivos e suplentes.

## Limitações

- Apenas reuniões plenárias. Presenças em comissões parlamentares não estão refletidas.
- Registos de efetivos e respetivos suplentes são contados separadamente.
- Os dados são tão fiáveis quanto a publicação oficial. Correções posteriores pelo Parlamento aparecem aqui no ciclo de ingestão seguinte.

## Licença

[MIT](LICENSE). Os dados são públicos e da responsabilidade do Parlamento.
