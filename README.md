# Mail Sentry: Sistema Inteligente de Categorização de E-mails

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-20.10.21-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Crew AI](https://img.shields.io/badge/Crew_AI-Powered-orange.svg)](https://github.com/joaomdmoura/crewAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Visão Geral

Mail Sentry é um sistema inteligente de categorização de e-mails que utiliza inteligência artificial para classificar automaticamente mensagens recebidas em categorias de prioridade. O sistema analisa o conteúdo, remetente e outros metadados dos e-mails para determinar sua relevância e urgência, permitindo uma gestão mais eficiente da comunicação por e-mail.

## 🏗️ Arquitetura do Sistema

O projeto Mail Sentry é composto por dois componentes principais:

1. **API de Categorização (pasta `/api`)**: Serviço baseado em FastAPI que recebe dados de e-mails e utiliza CrewAI para categorizá-los.

2. **Backend de Processamento (pasta `/backend`)**: Aplicação que se conecta a servidores de e-mail, recupera mensagens não lidas e as envia para a API de categorização.

```
Mail Sentry
├── api/                  # Serviço de categorização de e-mails
│   ├── api.py            # Endpoints da API FastAPI
│   ├── config.py         # Configurações da API
│   ├── Dockerfile        # Configuração para containerização
│   └── ...
└── backend/              # Processador de e-mails
    ├── app.py            # Lógica de conexão com servidores de e-mail
    ├── main.py           # Ponto de entrada da aplicação
    └── ...
```

### Diagrama de Fluxo

```
┌─────────────┐     ┌───────────────┐     ┌───────────────────┐       ┌─────────────┐
│  Servidor   │     │    Backend    │     │        API        │       │   Agente    │
│  de E-mail  │────▶│  Processador  │────▶│  de Categorização │────▶│   Crew AI   │
└─────────────┘     └───────────────┘     └───────────────────┘       └─────────────┘
       │                    │                      │                       │
       │                    │                      │                       │
       │                    │                      │                       │
       ▼                    ▼                      ▼                       ▼
┌─────────────┐     ┌───────────────┐     ┌───────────────────┐     ┌─────────────┐
│  E-mails    │     │ Extração de   │     │  Processamento    │     │ Categorias: │
│  não lidos  │────▶│ metadados e   │────▶│  e análise do     │────▶│ - URGENTE   │
│             │     │ conteúdo      │     │  conteúdo         │     │ - IMPORTANTE│
└─────────────┘     └───────────────┘     └───────────────────┘     │ - COMUM     │
                                                                    │ - LIXO      │
                                                                    └─────────────┘
```

## 🔄 Fluxo de Funcionamento

1. **Conexão com Servidores de E-mail**:
   - O backend se conecta a servidores IMAP (Gmail, Yahoo, etc.)
   - Recupera e-mails não lidos da caixa de entrada

2. **Processamento de E-mails**:
   - Extrai metadados (remetente, destinatário, assunto)
   - Processa o corpo do e-mail para extrair texto limpo
   - Prepara payload para envio à API

3. **Categorização com IA**:
   - A API recebe os dados do e-mail
   - Utiliza CrewAI para analisar o conteúdo
   - Classifica o e-mail em uma das categorias: URGENTE, IMPORTANTE, COMUM ou LIXO

4. **Ações Automatizadas**:
   - E-mails categorizados como LIXO são automaticamente marcados como lidos e excluídos
   - Outras categorias são processadas conforme configuração

## 🛠️ Tecnologias Utilizadas

### Backend de E-mail
- **[Python 3.12](https://www.python.org/)**: Linguagem de programação principal
- **[Imbox](https://github.com/martinrusev/imbox)**: Biblioteca para acesso a servidores IMAP
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)**: Processamento e limpeza de HTML
- **[Requests](https://requests.readthedocs.io/)**: Cliente HTTP para comunicação com a API
- **[python-dotenv](https://github.com/theskumar/python-dotenv)**: Gerenciamento de variáveis de ambiente

### API de Categorização
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web de alta performance
- **[CrewAI](https://github.com/joaomdmoura/crewAI)**: Framework para orquestração de agentes de IA
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Validação de dados e configurações
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para FastAPI

### Inteligência Artificial
- **[OpenAI API](https://openai.com/api/)**: Acesso a modelos de linguagem avançados
- **[LangChain](https://langchain.com/)**: Framework para desenvolvimento de aplicações com LLMs

### Infraestrutura
- **[Docker](https://www.docker.com/)**: Containerização da aplicação
- **[Docker Compose](https://docs.docker.com/compose/)**: Orquestração de containers

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.12+
- Docker e Docker Compose (para ambiente de produção)
- Acesso a contas de e-mail via IMAP
- Chave de API da OpenAI

### Configuração do Ambiente

1. Clone o repositório:
   ```bash
   git clone https://github.com/XSirch/mail-sentry.git
   cd mail-sentry
   ```

2. Configure as variáveis de ambiente:

   Para a API (crie o arquivo `api/.env`):
   ```
   ENVIRONMENT=development
   DEBUG=true
   OPENAI_API_KEY=sua_chave_api_aqui
   ```

   Para o Backend (crie o arquivo `backend/.env`):
   ```
   API_URL=http://localhost:8000/categorize
   YAHOO_USER=seu_email_yahoo@yahoo.com
   YAHOO_PASS=sua_senha_app_yahoo
   GOOGLE_USER=seu_email_gmail@gmail.com
   GOOGLE_PASS=sua_senha_app_gmail
   ```

   > **Nota**: Use senhas de aplicativo em vez de senhas regulares!

### Execução em Ambiente de Desenvolvimento

1. Configurar e iniciar a API:
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn api:app --reload
   ```

2. Configurar e iniciar o Backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

### Execução com Docker Compose

Para executar todo o sistema em containers Docker:

```bash
docker-compose up -d
```

Este comando iniciará tanto a API quanto o backend em containers separados.

## 🔍 Monitoramento e Logs

- **Logs da API**: `docker-compose logs -f api`
- **Logs do Backend**: `docker-compose logs -f backend`
- **Documentação da API**: Acesse `http://localhost:8000/docs` para a documentação interativa da API

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

Por favor, certifique-se de atualizar os testes conforme apropriado e seguir o estilo de código do projeto.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📬 Contato

- **Desenvolvedor**: [XSirch](https://github.com/XSirch)
- **E-mail**: seu-email@exemplo.com
- **Projeto**: [GitHub Repository](https://github.com/XSirch/mail-sentry)

---

<p align="center">
  <img src="https://img.shields.io/badge/Powered%20by-AI%20%2B%20Human%20Creativity-blue" alt="Powered by AI + Human Creativity">
</p>