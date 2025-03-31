import yfinance as yf

def fetch_option_data(ticker, expiration_date):
    """Récupère les données d'options pour un ticker donné."""
    option_data = yf.Ticker(ticker).option_chain(expiration_date)
    calls = option_data.calls
    puts = option_data.puts
    return calls, puts

def compare_with_black_scholes(calls, puts, S_market, r, sigma, T):
    """Compare les prix observés sur le marché avec le modèle Black-Scholes."""
    from black_scholes import black_scholes_call, black_scholes_put

    print("Comparaison Call:")
    for index, row in calls.iterrows():
        K = row['strike']
        market_price = row['lastPrice']
        bs_price = black_scholes_call(S_market, K, r, sigma, T)
        print(f"Strike: {K}, Prix marché: {market_price:.2f}, Prix Black-Scholes: {bs_price:.2f}")

    print("\nComparaison Put:")
    for index, row in puts.iterrows():
        K = row['strike']
        market_price = row['lastPrice']
        bs_price = black_scholes_put(S_market, K, r, sigma, T)
        print(f"Strike: {K}, Prix marché: {market_price:.2f}, Prix Black-Scholes: {bs_price:.2f}")