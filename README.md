# API de Upload e Download de Arquivos

API REST feita em Python + Flask que permite enviar (upload) e baixar (download) arquivos. Os arquivos são salvos na pasta `uploads/` e cada envio é registrado em `uploads.log`.

API no ar: https://ad-do-kauan.onrender.com

## Tecnologias

- Python 3
- Flask
- SQLite (banco criado automaticamente em `database.db`)
- Gunicorn (servidor usado em produção)
- Render (hospedagem)

## Estrutura do projeto

```
├── app.py                      # Cria o app Flask e registra as rotas
├── requirements.txt            # Dependências
├── controllers/
│   ├── upload_controller.py    # Regras do upload (extensão, tamanho, log)
│   └── download_controller.py  # Envia o arquivo para download
├── models/                     # Acesso ao banco de dados
├── routes/
│   ├── upload_route.py         # Rota de upload
│   └── download_route.py       # Rota de download
└── database/
    └── db.py                   # Conexão e criação da tabela SQLite
```

## Como rodar localmente

```bash
# 1. Clonar o repositório
git clone https://github.com/41891-ux/AD-do-kauan.git
cd SEU-REPOSITORIO

# 2. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar
python app.py
```

A API fica em `http://127.0.0.1:5000`.

## Rotas

| Método | Rota                      | Descrição                                      |
|--------|---------------------------|------------------------------------------------|
| GET    | `/`                       | Mostra que a API está no ar e lista as rotas   |
| POST   | `/uploads/upload`         | Envia um arquivo (campo `file`, `form-data`)   |
| GET    | `/downloads/<nome_arquivo>` | Baixa um arquivo que já foi enviado          |

### Regras do upload

- Extensões permitidas: `png`, `jpg`, `jpeg`, `gif`, `pdf`, `txt`
- Tamanho máximo: **30 KB**
- O nome do arquivo é limpo com `secure_filename` (remove caracteres perigosos)

### Exemplos

**Upload** (Postman: método POST, Body → form-data, chave `file` do tipo *File*)

```bash
curl -X POST -F "file=@teste.txt" https://ad-do-kauan.onrender.com
```

Resposta `200`:
```json
{ "mensagem": "Arquivo salvo com sucesso!", "arquivo": "teste.txt" }
```

Erros possíveis (`400`):
```json
{ "erro": "Nenhum arquivo enviado" }
{ "erro": "Nome do arquivo vazio" }
{ "erro": "Arquivo excede o tamanho máximo permitido (30 KB)" }
{ "erro": "Tipo de arquivo não permitido!", "tipos_permitidos": ["png", "jpg", "jpeg", "gif", "pdf", "txt"] }
```

**Download**

```bash
curl -O https://ad-do-kauan.onrender.com
```

Se o arquivo não existir (`404`):
```json
{ "error": "Arquivo não encontrado" }
```

## Deploy no Render

1. Subir o projeto para um repositório no GitHub.
2. No Render: **New → Web Service** e conectar o repositório.
3. Configurar:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Clicar em **Create Web Service** e aguardar o deploy.

## Observações

- No plano gratuito do Render o serviço "dorme" após alguns minutos sem uso; a primeira requisição depois disso pode levar cerca de 1 minuto.
- O disco do plano gratuito é **temporário**: os arquivos enviados e o `database.db` são apagados quando o serviço reinicia ou é reimplantado. Para guardar arquivos de forma permanente seria necessário um disco persistente ou um armazenamento externo.
