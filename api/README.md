# Crew AI Email Categorization API

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-20.10.21-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Crew AI](https://img.shields.io/badge/Crew_AI-Powered-orange.svg)](https://github.com/joaomdmoura/crewAI)

## Descrição

Esta API fornece um serviço de categorização de e-mails utilizando a tecnologia Crew AI. O sistema analisa e-mails recebidos e os categoriza automaticamente com base em seu conteúdo, remetente e outros metadados, permitindo uma gestão mais eficiente da comunicação por e-mail.

## Tecnologias Utilizadas

### Core
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web de alta performance para construção de APIs com Python
- **[CrewAI](https://github.com/joaomdmoura/crewAI)**: Framework para orquestração de agentes de IA colaborativos
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Validação de dados e configurações usando anotações de tipo Python
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI de alta performance para Python

### Inteligência Artificial
- **[OpenAI API](https://openai.com/api/)**: Acesso a modelos de linguagem avançados como GPT-4
- **[LangChain](https://langchain.com/)**: Framework para desenvolvimento de aplicações com LLMs

### Infraestrutura
- **[Docker](https://www.docker.com/)**: Containerização da aplicação
- **[Docker Compose](https://docs.docker.com/compose/)**: Orquestração de containers
- **[Nginx](https://nginx.org/)**: Servidor web e proxy reverso

### Monitoramento e Logging
- **[Prometheus](https://prometheus.io/)** (opcional): Monitoramento de métricas
- **[Grafana](https://grafana.com/)** (opcional): Visualização de métricas
- **[Sentry](https://sentry.io/)** (opcional): Rastreamento de erros

## Requisitos de Sistema

- Python 3.12+
- Docker e Docker Compose (para ambiente de produção)
- OpenAI API Key (para acesso aos modelos de linguagem)

## Dependências Principais

- FastAPI: Framework web de alta performance
- CrewAI: Framework para orquestração de agentes de IA
- Uvicorn: Servidor ASGI para FastAPI
- Pydantic: Validação de dados e configurações

## Estrutura de Arquivos

```
api/
├── Dockerfile              # Configuração para containerização
├── docker-compose.yml      # Configuração para orquestração de containers
├── requirements.txt        # Dependências Python
├── api.py                  # Ponto de entrada da aplicação e definição de endpoints
├── config.py               # Configurações da aplicação
├── .env                    # Variáveis de ambiente (não versionado)
├── .env.example            # Exemplo de variáveis de ambiente
└── README.md               # Este arquivo
```

## Instalação e Configuração

### Ambiente de Desenvolvimento

1. Clone o repositório:
   ```bash
   git clone https://github.com/XSirch/mail-sentry.git
   cd mail-sentry/api
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` baseado no `.env.example`:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. Execute a aplicação:
   ```bash
   uvicorn api:app --reload
   ```

6. Acesse a documentação da API em `http://localhost:8000/docs`

### Ambiente de Produção (VPS)

1. Transfira os arquivos para a VPS:
   ```bash
   # Usando SCP
   scp -r api/ usuario@seu-servidor:/caminho/para/deploy/
   
   # Ou clone o repositório diretamente na VPS
   ssh usuario@seu-servidor
   git clone https://github.com/XSirch/mail-sentry.git
   ```

2. Configure as variáveis de ambiente:
   ```bash
   cd /caminho/para/deploy/api
   cp .env.example .env
   nano .env  # Edite com as configurações de produção
   ```

3. Construa e inicie os containers:
   ```bash
   docker-compose up -d --build
   ```

4. Verifique se a aplicação está rodando:
   ```bash
   docker-compose ps
   curl http://localhost:8000/health
   ```

## Execução com Docker

### Construir a imagem
```bash
docker build -t email-categorization-api .
```

### Executar o container
```bash
docker run -p 8000:8000 --env-file .env email-categorization-api
```

### Usando Docker Compose
```bash
# Iniciar serviços
docker-compose up -d

# Verificar logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

## Endpoints da API

### Verificação de Saúde
```
GET /health
```
Retorna o status da API.

### Categorização de E-mail
```
POST /categorize
```
Recebe um e-mail e retorna sua categorização.

Exemplo de payload:
```json
{
  "de": "cliente@empresa.com",
  "para": "suporte@minhaempresa.com",
  "assunto": "Problema com faturamento",
  "corpo": "Olá, estou com dificuldades para acessar minha fatura deste mês..."
}
```

## Troubleshooting

### A API não está iniciando

1. Verifique se todas as variáveis de ambiente estão configuradas corretamente:
   ```bash
   cat .env
   ```

2. Verifique se a chave da API OpenAI é válida:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

3. Verifique os logs do container:
   ```bash
   docker-compose logs -f
   ```

### Erros de conexão com a API

1. Verifique se o container está rodando:
   ```bash
   docker ps
   ```

2. Verifique se a porta está corretamente mapeada:
   ```bash
   docker-compose ps
   ```

3. Teste a conexão localmente:
   ```bash
   curl http://localhost:8000/health
   ```

## Contribuição

Para contribuir com este projeto:

1. Crie um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Contato

Para questões ou suporte, entre em contato com:
- GitHub: [XSirch](https://github.com/XSirch)
