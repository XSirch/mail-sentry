# Mail Categorizer Backend

Este é o backend do sistema de categorização de emails usando imbox.

## Estrutura

```
backend/
├── app.py              # Classe principal do categorizador
├── main.py             # Script de entrada
├── requirements.txt    # Dependências Python
├── Dockerfile          # Configuração Docker
├── docker-compose.yml  # Orquestração de containers
├── .dockerignore       # Arquivos ignorados no build
├── .env.example        # Exemplo de variáveis de ambiente
└── README.md          # Este arquivo
```

## Configuração

### 1. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais reais:

```env
# Email Configuration
YAHOO_USER=seu_email@yahoo.com
YAHOO_PASS=sua_senha_de_app_yahoo
GOOGLE_USER=seu_email@gmail.com
GOOGLE_PASS=sua_senha_de_app_gmail
API_URL=http://api:8000/categorize
```

### 2. Senhas de Aplicativo

**Para Gmail:**
1. Ative a autenticação de 2 fatores
2. Vá em "Senhas de app" nas configurações da conta Google
3. Gere uma senha específica para este aplicativo

**Para Yahoo:**
1. Ative a autenticação de 2 fatores
2. Vá em configurações de segurança da conta Yahoo
3. Gere uma senha de aplicativo

## Execução com Docker

### Build da Imagem

```bash
docker build -t mail-categorizer-backend .
```

### Execução Simples

```bash
docker run --env-file .env mail-categorizer-backend
```

### Execução com Docker Compose

```bash
# Subir todos os serviços (backend + API)
docker-compose up -d

# Ver logs
docker-compose logs -f mail-categorizer

# Parar serviços
docker-compose down
```

### Execução em Desenvolvimento

```bash
# Build e execução em modo desenvolvimento
docker-compose up --build

# Executar apenas uma vez (sem loop)
docker run --env-file .env mail-categorizer-backend python main.py
```

## Funcionalidades

- **Conexão IMAP**: Conecta aos servidores Gmail e Yahoo
- **Processamento de Emails**: Lê emails não lidos
- **Limpeza de Conteúdo**: Remove HTML e formata texto
- **Categorização**: Envia para API de categorização
- **Ações Automáticas**: Marca como lido e exclui emails categorizados como "LIXO"

## Logs

Os logs são salvos no diretório `./logs` quando executado via Docker Compose.

## Troubleshooting

### Erro de Autenticação
- Verifique se as senhas de aplicativo estão corretas
- Confirme que a autenticação de 2 fatores está ativada
- Teste as credenciais manualmente

### Erro de Conexão
- Verifique a conectividade de rede
- Confirme que as portas IMAP estão abertas (993 para SSL)
- Teste a conexão com telnet: `telnet imap.gmail.com 993`

### API Não Encontrada
- Verifique se o serviço da API está rodando
- Confirme a URL da API no arquivo .env
- Teste a API diretamente: `curl http://localhost:8000/health`

## Desenvolvimento

Para desenvolvimento local sem Docker:

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```
