# Manhwas — leitor estático

Catálogo e leitor vertical de manhwas, hospedados no GitHub Pages, com imagens em pastas públicas do Google Drive.

## Publicação
Em **Settings → Pages → Build and deployment**, escolha **GitHub Actions**. O workflow `pages.yml` publica o site automaticamente a cada push na main.

## Atualização automática do catálogo
Crie uma chave da **Google Drive API v3** em Google Cloud (API ativada e chave restrita à Drive API). No GitHub, adicione o secret de Actions **DRIVE_API_KEY**. O workflow `sync.yml` consulta as pastas públicas diariamente e atualiza `catalog.json` sem armazenar a chave no frontend.

Organização no Drive: pasta principal = obra; subpastas "Capítulo 01", "Capítulo 02" etc.; imagens "Pagina_01.png" etc. Outras obras podem ser adicionadas em `sources.json`. Arquivos DOCX e XLSX são ignorados.

Sem a chave, o catálogo inicial contém o Capítulo 01 já cadastrado e o site funciona imediatamente, desde que as imagens estejam públicas.

## Recorte
O leitor detecta margens brancas com Canvas quando o host da imagem permite leitura de pixels (CORS). Se não permitir, aplica recorte visual configurável, sem alterar os arquivos originais.

## URLs
`/#/` catálogo; `/#/obra/dragao-oculto` capítulos; `/#/ler/dragao-oculto/1` leitor.

MIT — código do leitor. Imagens e histórias permanecem sob direitos de seus respectivos autores.
