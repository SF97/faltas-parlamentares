# Astro Starter Kit: Minimal

```sh
pnpm create astro@latest -- --template minimal
```

> 🧑‍🚀 **Seasoned astronaut?** Delete this file. Have fun!

## 🚀 Project Structure

Inside of your Astro project, you'll see the following folders and files:

```text
/
├── public/
├── src/
│   └── pages/
│       └── index.astro
└── package.json
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro/React/Vue/Svelte/Preact components.

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `pnpm install`             | Installs dependencies                            |
| `pnpm dev`             | Starts local dev server at `localhost:4321`      |
| `pnpm build`           | Build your production site to `./dist/`          |
| `pnpm preview`         | Preview your build locally, before deploying     |
| `pnpm astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `pnpm astro -- --help` | Get help using the Astro CLI                     |

## 👀 Want to learn more?

Feel free to check [our documentation](https://docs.astro.build) or jump into our [Discord server](https://astro.build/chat).

## Percentagem de faltas

O site calcula `100 × (FJ + FI + F) / (FJ + FI + F + P + AMP + PNO + FQV)`
a partir dos totais nos ficheiros de detalhe dos deputados, através de
`src/lib/absence.ts`. FJ, FI e F são faltas; P, AMP e PNO são presença ou trabalho
parlamentar. FQV conta como presença para esta percentagem porque o deputado
esteve presente, embora não tenha participado no número mínimo de votações.
A classificação FQV continua a ser apresentada separadamente.

Os valores por grupo parlamentar e para toda a AR aplicam a fórmula às contagens
somadas dos deputados do ranking da XVII Legislatura, mantendo os grupos dos
dados atuais. Não são médias aritméticas das percentagens individuais. Os registos
de efetivos e suplentes continuam separados.

A apresentação usa uma casa decimal e o formato `pt-PT`; a ordenação usa o valor
sem arredondamento. Sem registos nas sete categorias, o cálculo devolve `null` e
a interface mostra «—» com explicação; estes valores ficam no fim da ordenação
em ambos os sentidos. Faltas não classificadas podem ser reclassificadas em
atualizações posteriores. A explicação pública está em
`/metodologia#percentagem-de-faltas`.
