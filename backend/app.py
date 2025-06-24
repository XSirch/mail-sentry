from imbox import Imbox
from datetime import datetime
from bs4 import BeautifulSoup
import re
import requests
import os

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
                        # 3.2 — colapsa 2+ blank lines para no máximo 1
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
                        api_url = os.environ["API_URL"]
                        payload = {
                            "de": de,
                            "para": para,
                            "assunto": assunto,
                            "corpo": texto
                        }
                        response = requests.post(api_url, json=payload)
                        if response.status_code == 200:
                            categoria = response.json()["categoria"]
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
                        else:
                            print(f"Erro ao categorizar: {response.text}")
                    except Exception as e:
                        print(f"Erro ao processar mensagem: {e}")
            return                
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            return False
        