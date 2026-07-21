# Gerador de Landing Pages — System Digital

Gera uma LP por cliente, cada uma em um diretório do seu domínio:
`lp.gruposystemdigital.com.br/daliene`, `/fraciele`, etc.

## Estrutura
```
(raiz do repositório) = o que vai pro GitHub Pages
├── CNAME                     -> lp.gruposystemdigital.com.br
├── editor.html              -> EDITOR VISUAL (lp.gruposystemdigital.com.br/editor.html)
├── fraciele/                 -> LP publicada (index.html)
└── gerador/                  -> a "fábrica" (código-fonte do gerador)
    ├── template.html         -> modelo da LP (tokens {{NOME}}, {{WHATSAPP}}...)
    ├── _editor_shell.html    -> interface do editor
    ├── build_editor.py       -> monta o editor.html (template + interface)
    ├── publish.py            -> instala uma LP exportada em /<slug>/
    ├── build.py              -> gerador antigo por linha de comando
    └── clientes/daliene/     -> exemplo (config.json + assets)
```

## Configuração (uma vez só)
1. Crie um repositório no GitHub e suba estes arquivos.
2. **Settings > Pages**: Deploy from a branch → `main` → `/root`.
3. Em **Settings > Pages > Custom domain**, coloque `lp.gruposystemdigital.com.br`.
4. No seu provedor de DNS, crie um registro **CNAME**:
   `lp`  →  `SEU-USUARIO.github.io`
5. Aguarde o certificado HTTPS ficar verde (alguns minutos).

## Editor visual (jeito principal — tipo WordPress)
Abra **`editor.html`** no navegador (ou pelo site: `lp.gruposystemdigital.com.br/editor.html`).
- Formulário à esquerda, preview da LP ao vivo à direita.
- Seções: Identidade, **Design (cores/fontes/temas)**, Contato (com **Meta Pixel** e
  mensagem do WhatsApp), Localização, Textos (bio & local), **✍️ Textos das seções
  (63 campos: todos os títulos, botões, selos, itens e avisos da página)**,
  Imagens, Casos, Depoimentos, FAQ e Espaço.
- Em "Textos das seções", `*asteriscos*` viram itálico serifado, e os campos aceitam
  `{{NOME}}`, `{{NOME_CURTO}}` e `{{CIDADE_UF}}`. Campo vazio = texto padrão.
- Botões:
  - **Exportar index.html** → baixa `<slug>.html` (arquivo único, imagens embutidas, pixel incluso).
  - **Salvar projeto** → baixa `<slug>.json` (reeditável — reabra depois em "Abrir projeto").

O **Slug** (seção Identidade) define a URL final: `lp.gruposystemdigital.com.br/<slug>`.

## Publicar uma LP
1. No editor, preencha o **Slug** e clique **Exportar index.html** → gera `fraciele.html`.
2. Rode o publicador (instala em `/fraciele/index.html`):
   ```
   python gerador/publish.py caminho/para/fraciele.html
   ```
3. Suba:
   ```
   git add . && git commit -m "LP fraciele" && git push
   ```
   No ar em ~1 min: `lp.gruposystemdigital.com.br/fraciele`

## Manutenção do editor
O `editor.html` é gerado a partir de `gerador/_editor_shell.html` (interface) +
`gerador/template.html` (o modelo da LP, embutido em base64). Se mudar qualquer um:
```
python gerador/build_editor.py
```

## Tokens do template (referência)
`{{NOME}}`, `{{NOME_CURTO}}`, `{{WHATSAPP}}`, `{{WA_MSG}}`, `{{INSTAGRAM}}`, `{{ESPECIALIDADE}}`,
`{{CIDADE_UF}}`, `{{ENDERECO}}`, `{{BIO}}`, `{{LOCAL_DESC}}`, `{{MAPS_LINK}}`, `{{MAPS_EMBED}}`
+ 63 tokens de texto `{{T_*}}` (ex.: `{{T_HERO_TITLE}}`, `{{T_MET_TAG}}`, `{{T_FOOT_COPY}}`),
definidos em `TEXT_GROUPS` dentro de `_editor_shell.html`
+ marcadores de lista `<!--DEPOIMENTOS-->`, `<!--FAQ-->`, `<!--CASOS-->`, `<!--ESPACO-->`.
O editor preenche tudo isso automaticamente. O antigo `gerador/build.py` (via `config.json`)
continua para o fluxo por linha de comando, mas o editor é o caminho recomendado.
