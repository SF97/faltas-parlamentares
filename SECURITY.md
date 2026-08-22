# Política de segurança / Security policy

## Português (PT-PT)

### Versões suportadas

O faltas-parlamentares é um site continuamente atualizado e não publica
versões numeradas. Apenas o código presente no ramo predefinido e o site
atualmente publicado recebem correções de segurança.

Versões históricas, forks e instalações modificadas por terceiros não são
suportados.

### Comunicar uma vulnerabilidade

Não abra um issue público para comunicar uma possível vulnerabilidade.

Utilize a opção **Report a vulnerability** em **Security → Advisories** neste
repositório para [comunicar uma vulnerabilidade de forma
privada](https://github.com/SF97/faltas-parlamentares/security/advisories/new).
A comunicação pode ser feita em português ou inglês.

Inclua, sempre que possível:

- o componente afetado;
- uma descrição do impacto;
- os passos necessários para reproduzir o problema;
- uma prova de conceito que não seja destrutiva;
- possíveis medidas de correção ou mitigação.

Não inclua credenciais, dados pessoais ou outros dados sensíveis
desnecessários no relatório.

Procurarei confirmar a receção do relatório o mais rápido possível. Peço que
aguarde uma correção ou uma divulgação coordenada antes de publicar detalhes.

### Âmbito

Exemplos de problemas de segurança relevantes:

- execução ou injeção de código através dos dados ingeridos;
- vulnerabilidades que afetem o site publicado;
- comprometimento do pipeline de ingestão ou do workflow de publicação;
- exposição de credenciais ou permissões indevidas;
- vulnerabilidades exploráveis nas dependências utilizadas pelo projeto.

Os seguintes problemas devem ser comunicados através de uma issue normal:

- dados parlamentares incorretos, incompletos ou desatualizados;
- alterações no HTML do parlamento.pt que quebrem o parser;
- erros de classificação ou apresentação;
- indisponibilidade das fontes oficiais.

### Investigação responsável

Ao investigar uma possível vulnerabilidade:

- não aceda, altere ou destrua dados de terceiros;
- não interrompa o site, o repositório ou serviços externos;
- utilize apenas o acesso necessário para demonstrar o problema;
- dê tempo razoável para investigar e corrigir o problema.

Este projeto não mantém um programa de recompensas.

---

## English

### Supported versions

faltas-parlamentares is continuously updated and does not publish numbered
releases. Only the code on the default branch and the currently deployed site
receive security fixes.

Historical versions, forks, and third-party modified installations are not
supported.

### Reporting a vulnerability

Do not open a public issue to report a potential vulnerability.

Use **Report a vulnerability** under **Security → Advisories** in this
repository to [report a vulnerability
privately](https://github.com/SF97/faltas-parlamentares/security/advisories/new).
Reports may be submitted in Portuguese or English.

Whenever possible, include:

- the affected component;
- a description of the impact;
- the steps required to reproduce the issue;
- a non-destructive proof of concept;
- possible fixes or mitigations.

Do not include credentials, personal data, or other unnecessary sensitive
information in the report.

I will aim to acknowledge the report as fast as possible. Please allow time for a
fix or coordinated disclosure before publishing details.

### Scope

Examples of relevant security issues include:

- code execution or injection through ingested data;
- vulnerabilities affecting the deployed site;
- compromise of the ingestion pipeline or publishing workflow;
- exposure of credentials or excessive permissions;
- exploitable vulnerabilities in the project's dependencies.

The following should be reported through a regular issue:

- incorrect, incomplete, or outdated parliamentary data;
- changes to the parlamento.pt HTML that break the parser;
- classification or presentation errors;
- unavailability of official upstream sources.

### Responsible research

When investigating a potential vulnerability:

- do not access, modify, or destroy third-party data;
- do not disrupt the site, repository, or external services;
- use only the access necessary to demonstrate the issue;
- allow reasonable time to investigate and fix the issue.

This project does not currently operate a bug bounty program.
