
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from config import settings
import crewai
import os
import json

app = FastAPI(
    title="Crew AI Email Categorization API",
    description="API categorização de e-mails com Crew AI",
    version="0.1.0",
    debug=settings.debug
)
llm = crewai.LLM("gpt-4.1-nano", temperature=0.2, api_key=os.environ["OPENAI_API_KEY"])


class EmailPayload(BaseModel):
    de: str = Field(..., description="Endereço do remetente")
    para: str = Field(..., description="Endereço do destinatário")
    assunto: str = Field(..., description="Assunto do e-mail")
    corpo: str = Field(..., description="Conteúdo do e-mail")

class CategorizationResponse(BaseModel):
    categoria: str = Field(..., description="Categoria: Lixo, Comum, Importante ou Urgente")

async def categorizar(email: EmailPayload) -> str:
    payload = {
        "de": email.de,
        "para": email.para, 
        "assunto": email.assunto,
        "corpo": email.corpo
    }
    print(f"Dados do email enviados para categorização: {payload}")
    agente = crewai.Agent(
        llm=llm,
        name="Categorizador de E-mails",
        role="Analista Especializado em Triagem de E-mails",
        goal="Categorizar e-mails com precisão, identificando corretamente a prioridade e relevância de cada mensagem",
        backstory="""Você é um especialista em análise e triagem de e-mails com anos de experiência.
Você desenvolveu um sistema preciso para categorizar e-mails em quatro categorias:

1. URGENTE: E-mails que exigem atenção imediata. Características:
   - Contém palavras como "URGENTE", "EMERGÊNCIA", "IMEDIATO" no assunto
   - Remetentes são pessoas importantes (chefes, clientes VIP)
   - Conteúdo indica prazos iminentes ou situações críticas
   - Solicitações explícitas de resposta rápida

2. IMPORTANTE: E-mails que são relevantes mas não críticos. Características:
   - Remetentes são colegas de trabalho, parceiros de negócios
   - Assuntos relacionados a projetos, reuniões ou tarefas significativas
   - Conteúdo contém informações relevantes para o trabalho
   - Prazos mais longos ou sem urgência explícita

3. COMUM: E-mails rotineiros sem prioridade especial. Características:
   - Comunicações do dia-a-dia
   - Atualizações gerais
   - Informações que não exigem ação imediata
   - Newsletters relevantes

4. LIXO: E-mails indesejados ou de baixa relevância. Características:
   - Marketing em massa
   - Promoções não solicitadas
   - Remetentes desconhecidos com conteúdo genérico
   - Assuntos com excesso de pontuação ou CAPS LOCK
   - Conteúdo irrelevante para o destinatário

Sua análise é altamente valorizada porque você consegue identificar nuances sutis que determinam a verdadeira categoria de cada e-mail."""
    )
    task = crewai.Task(
        description="""Analise cuidadosamente o e-mail fornecido
            De: {{de}}
            Para: {{para}}
            Assunto: {{assunto}}
            Corpo:
            {{corpo}}

            e categorize-o como LIXO, COMUM, IMPORTANTE ou URGENTE.

Siga estas diretrizes específicas:
1. Examine o REMETENTE: Considere a relevância e importância do remetente.
2. Analise o ASSUNTO: Procure palavras-chave como "urgente", "importante", prazos ou solicitações específicas.
3. Avalie o CONTEÚDO: Determine a relevância, urgência e importância do conteúdo.

CRITÉRIOS ESPECÍFICOS:
- URGENTE: Mensagens que exigem atenção imediata, contêm palavras como "urgente" no assunto, mencionam prazos iminentes ou são de remetentes de alta prioridade.
- IMPORTANTE: Mensagens relevantes para trabalho/projetos, de remetentes significativos, mas sem necessidade de ação imediata.
- COMUM: Comunicações rotineiras, informativas, sem ação específica necessária.
- LIXO: Promoções não solicitadas, marketing em massa, mensagens irrelevantes ou potencialmente maliciosas.

Responda APENAS com uma das quatro categorias: LIXO, COMUM, IMPORTANTE ou URGENTE.""",
        expected_output="LIXO, COMUM, IMPORTANTE ou URGENTE",
        agent=agente
    )
    crew = crewai.Crew(
        agents=[agente],
        tasks=[task],
        process=crewai.Process.sequential,
        verbose=True
    )
    result = crew.kickoff(inputs=payload)
    print(f"Dados do email enviados para categorização: {payload}")

    if isinstance(result, dict):
            categoria = (
                result.get("categoria")
                or result.get("Categoria")
                or result.get("Category")
            )
    else:
        categoria = result

    # 4) Garante que seja string
    if not isinstance(categoria, str):
        categoria = str(categoria)

    categoria = categoria.strip().upper()
    if "URGENTE" in categoria:
        return "URGENTE"
    elif "IMPORTANTE" in categoria:
        return "IMPORTANTE"
    elif "COMUM" in categoria:
        return "COMUM"
    elif "LIXO" in categoria:
        return "LIXO"
    else:
        # Se não conseguir identificar, retorna a resposta original
        return categoria

@app.post("/categorize", response_model=CategorizationResponse)
async def categorize_email(request: Request):
    # parsing robusto do body JSON
    raw = await request.body()
    payload_dict = None
    for enc in ("utf-8", "latin-1"):
        try:
            text = raw.decode(enc)
            payload_dict = json.loads(text)
            break
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    if payload_dict is None:
        text = raw.decode("utf-8", errors="replace")
        raise HTTPException(status_code=400, detail={
            "error": "JSON inválido",
            "raw_body": text
        })
    # valida e converte em EmailPayload
    try:
        email = EmailPayload(**payload_dict)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    # categoriza
    try:
        categoria = await categorizar(email)
        return {"categoria": categoria}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para debug
@app.post("/debug")
async def debug_request(request: Request):
    raw = await request.body()
    text = None
    # tenta primeiro UTF-8, depois Latin-1
    for enc in ("utf-8", "latin-1"):
        try:
            text = raw.decode(enc)
            payload = json.loads(text)
            return {"received_json": payload}
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue

    # se ainda não conseguiu, mostra o raw com substituições
    text = raw.decode("utf-8", errors="replace")
    return {
        "error": "não foi possível parsear JSON nem em UTF-8 nem Latin-1",
        "raw_body": text
    }

@app.get("/")
async def root():
    return {"message": "API funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}