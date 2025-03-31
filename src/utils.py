from tenacity import retry, stop_after_attempt, wait_fixed
import yfinance as yf

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def fetch_option_data(ticker, expiration_date):
    """
    Récupère les données d'options pour un ticker donné et une date d'échéance.
    Réessaie jusqu'à 5 fois en cas d'erreur, avec un délai de 2 secondes entre chaque tentative.
    """
    try:
        option_data = yf.Ticker(ticker).option_chain(expiration_date)
        return option_data.calls, option_data.puts
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des données : {e}")