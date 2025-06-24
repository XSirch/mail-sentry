from imbox import Imbox
from datetime import datetime
from bs4 import BeautifulSoup
import re
import requests
import os
import time

class Categorizador:
    def __init__(self, servidor, usuario, senha):
        self.servidor = servidor
        self.usuario = usuario
        self.senha = senha
        self.conexao = None
        
    def conectar_email(self):
        try:
            with Imbox(self.servidor, self.usuario, self.senha, ssl=True, ssl_context=None, starttls=False) as imbox:
                unread_inbox_messages = imbox.messages(unread=True)
                for uid, message in unread_inbox_messages:
                    try:
                        # 1) Metadados
                        de      = ", ".join(f"{f['name']} <{f['email']}>" for f in message.sent_from)
                        para    = ", ".join(f"{f['name']} <{f['email']}>" for f in message.sent_to)
                        assunto = message.subject or "(sem assunto)"
                        data    = message.date or datetime.now()

                        # 2) Corpo “limpo”
                        html = message.body.get('html', [])
                        if isinstance(html, list) and html:
                            raw = "\n".join(html)
                            texto = BeautifulSoup(raw, "html.parser").get_text(separator="\n")
                        else:
                            # Cai no plain
                            plain = message.body.get('plain', [])
                            if isinstance(plain, list):
                                texto = "\n".join(plain)
                            else:
                                texto = plain or ""
                        # converte CRLF em LF e remove espaços desnecessários
                        soup = BeautifulSoup(texto, "html.parser")
                        texto = soup.get_text(separator="\n").strip()
                        lines = [line.strip() for line in texto.splitlines()]
                        texto = "\n".join(lines)
                        texto = re.sub(r'\n{2,}', '\n\n', texto).strip()

                        # 3) Impressão formatada
                        print("="*80)
                        print(f"De:      {de}")
                        print(f"Para:    {para}")
                        print(f"Assunto: {assunto}")
                        print(f"Data:    {data}")
                        print("-"*80)
                        print(texto)
                        print("="*80 + "\n")

                        # 4) Envia para a API de categorização
                        payload = {
                            "de": de,
                            "para": para,
                            "assunto": assunto,
                            "corpo": texto
                        }
                        response = self.enviar_para_api(payload)
                        categoria = response.get("categoria", "DESCONHECIDO")
                        print(f"Categoria: {categoria}")

                        if categoria == "LIXO":
                            try:
                                imbox.mark_seen(uid)
                                imbox.delete(uid)
                                print("E-mail marcado como lido e excluído.")
                                # mostra quantos emails restam
                                print(f"Restam {len(imbox.messages(unread=True))} emails para processar.")
                            except Exception as e:
                                print(f"Erro ao marcar como lido e excluir: {e}")
                        if categoria == "COMUM":
                            try:
                                imbox.mark_seen(uid)
                                print("E-mail marcado como lido.")
                                # mostra quantos emails restam
                                print(f"Restam {len(imbox.messages(unread=True))} emails para processar.")
                            except Exception as e:
                                print(f"Erro ao marcar como lido: {e}")
                        if categoria == "IMPORTANTE":
                            try:
                                self.mover_email(uid, categoria)
                            except Exception as e:
                                print(f"Erro ao mover para pasta {categoria}: {e}")
                        if categoria == "URGENTE":
                            try:
                                self.mover_email(uid, categoria)
                            except Exception as e:
                                print(f"Erro ao mover para pasta {categoria}: {e}")
                    except Exception as e:
                        print(f"Erro ao processar mensagem: {e}")
            return  categoria          
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            return False

    def enviar_para_api(self, email_data):
        max_retries = 3
        retry_delay = 3  # segundos
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    os.getenv("API_URL", "http://api:8000/categorize"),
                    json=email_data,
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Tentativa {attempt+1}/{max_retries} falhou: {e}")
                if attempt < max_retries - 1:
                    print(f"Tentando novamente em {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    print("API indisponível após várias tentativas. Continuando processamento...")
                    return {"categoria": "DESCONHECIDO", "confianca": 0}
        
    def mover_email(self,uid, categoria):
        import imaplib
        # 1) Abre conexão IMAP
        imap = imaplib.IMAP4_SSL(self.servidor, 993)
        imap.login(self.usuario, self.senha)

        # 2) Seleciona a pasta INBOX
        imap.select("INBOX")

        # 3) Garanta que a pasta exista
        destino = categoria.capitalize()  # "Urgente", "Importante" etc.
        imap.create(destino)              # silencia erro se já existir

        # 4) Move a mensagem
        try:
            imap.uid("MOVE", uid, destino)
        except imaplib.IMAP4.error:
            # fallback: COPY + STORE + EXPUNGE
            imap.uid("COPY", uid, destino)
            imap.uid("STORE", uid, "+FLAGS", r"(\Deleted)")
            imap.expunge()

        print(f"UID {uid.decode()} movido para {destino}")

        # 7) Logout
        imap.close()
        imap.logout()