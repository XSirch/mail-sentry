from app import Categorizador
from dotenv import load_dotenv
import os

load_dotenv()
class Start:
    def yahoo():
        try:
            categorizador = Categorizador("imap.mail.yahoo.com", os.getenv("YAHOO_USER"), os.getenv("YAHOO_PASS"))
            categorizador.conectar_email()
        except Exception as e:
            print(f"Erro ao conectar ao Yahoo: {e}")

    def google():
        try:
            categorizador = Categorizador("imap.gmail.com", os.getenv("GOOGLE_USER"), os.getenv("GOOGLE_PASS"))
            categorizador.conectar_email()
        except Exception as e:
            print(f"Erro ao conectar ao Google: {e}")



if __name__ == "__main__":
    Start.google()
    print("Google terminou")
    
