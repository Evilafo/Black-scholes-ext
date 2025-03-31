import numpy as np

def binomial_tree_option(S, K, r, sigma, T, N, option_type="call"):
    """Calcule le prix d'une option européenne avec un arbre binomial."""
    dt = T / N  # Pas de temps
    u = np.exp(sigma * np.sqrt(dt))  # Facteur de hausse
    d = 1 / u  # Facteur de baisse
    p = (np.exp(r * dt) - d) / (u - d)  # Probabilité risque-neutre

    # Initialiser les prix finaux de l'actif sous-jacent
    stock_prices = np.zeros(N + 1)
    for i in range(N + 1):
        stock_prices[i] = S * (u**i) * (d**(N - i))

    # Calculer les payoffs finaux
    option_values = np.zeros(N + 1)
    if option_type == "call":
        option_values = np.maximum(stock_prices - K, 0)
    elif option_type == "put":
        option_values = np.maximum(K - stock_prices, 0)

    # Propagation rétrograde
    for step in range(N - 1, -1, -1):
        for i in range(step + 1):
            option_values[i] = np.exp(-r * dt) * (p * option_values[i + 1] + (1 - p) * option_values[i])

    return option_values[0]