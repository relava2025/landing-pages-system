# Gerador de Landing Pages — System Digital

Gera uma LP por cliente, cada uma em um diretório do seu domínio:
`lp.gruposystemdigital.com.br/daliene`, `/fraciele`, etc.

## Estrutura
```
(raiz do repositório) = o que vai pro GitHub Pages
├── CNAME                     -> lp.gruposystemdigital.com.br
├── daliene/                  -> LP GERADA (index.html + imagens)
├── fraciele/                 -> LP GERADA
└── gerador/                  -> NÃO aparece no site, é a "fábrica"
    ├── template.html         -> o modelo com campos {{NOME}}, {{WHATSAPP}}...
    ├── build.py              -> gera a pasta do cliente
    └── clientes/
        └── daliene/
            ├── config.json   -> textos/dados do cliente
            └── assets/       -> imagens do cliente
```

## Configuração (uma vez só)
1. Crie um repositório no GitHub e suba estes arquivos.
2. **Settings > Pages**: Deploy from a branch → `main` → `/root`.
3. Em **Settings > Pages > Custom domain**, coloque `lp.gruposystemdigital.com.br`.
4. No seu provedor de DNS, crie um registro **CNAME**:
   `lp`  →  `SEU-USUARIO.github.io`
5. Aguarde o certificado HTTPS ficar verde (alguns minutos).

## Criar uma LP nova (o dia a dia)
1. Duplique a pasta `gerador/clientes/daliene` e renomeie para o slug do cliente
   (ex.: `gerador/clientes/fraciele`).
2. Edite o `config.json` com os dados dele (nome, WhatsApp, bio, local).
3. Coloque as imagens em `assets/images/` (veja os nomes no arquivo
   `_COLOQUE-AS-IMAGENS-AQUI.txt`).
4. Rode:
   ```
   python gerador/build.py fraciele
   ```
   Isso cria a pasta `/fraciele/` na raiz, pronta.
5. Publique:
   ```
   git add .
   git commit -m "LP fraciele"
   git push
   ```
   No ar em ~1 min: `lp.gruposystemdigital.com.br/fraciele`

## Campos do config.json
- `NOME`        -> nome completo (ex.: "Dra. Daliene Electo")
- `NOME_CURTO`  -> nome curto (ex.: "Dra. Daliene")
- `WHATSAPP`    -> só números, com DDI (ex.: "554989001311")
- `BIO`         -> parágrafo da seção "Conheça a Dra."
- `LOCAL_DESC`  -> parágrafo da seção "Local de atuação"
- `DEPOIMENTOS` -> lista de avaliações: cada item tem `texto` e `autor`
                  (o gerador duplica a lista sozinho p/ o scroll do mobile)
- `FAQ`         -> lista de perguntas: cada item tem `pergunta` e `resposta`
                  (pode usar {{NOME_CURTO}} dentro do texto que ele resolve)

Agora o `config.json` cobre TUDO que muda por cliente: nome, WhatsApp, bio,
local, depoimentos e FAQ. Só as imagens ficam de fora (vão na pasta assets).
