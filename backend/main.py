from app import Categorizador
import os

if __name__ == "__main__":
    categorizador = Categorizador("imap.mail.yahoo.com", os.environ("YAHOO_USER"), os.environ("YAHOO_PASS"))
    print(os.getenv("YAHOO_USER"), os.environ("YAHOO_PASS"))
    categorizador.conectar_yahoo()
