import numpy as np
from scipy.stats import norm

def calculate_d1_d2(S, K, r, sigma, T):
    """Calcule d1 et d2 pour le modèle Black-Scholes."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def black_scholes_call(S, K, r, sigma, T):
    """Calcule le prix d'un call européen avec Black-Scholes."""
    d1, d2 = calculate_d1_d2(S, K, r, sigma, T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, r, sigma, T):
    """Calcule le prix d'un put européen avec Black-Scholes."""
    d1, d2 = calculate_d1_d2(S, K, r, sigma, T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price