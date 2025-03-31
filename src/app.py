import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from utils import fetch_option_data  # Importer la fonction depuis utils.py

# Fonctions Black-Scholes
def calculate_d1_d2(S, K, r, sigma, T):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def black_scholes_call(S, K, r, sigma, T):
    d1, d2 = calculate_d1_d2(S, K, r, sigma, T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, r, sigma, T):
    d1, d2 = calculate_d1_d2(S, K, r, sigma, T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

# Titre de l'application
st.title("Modèle Black-Scholes pour évaluer des options")

# Entrées utilisateur
st.sidebar.header("Paramètres")
S = st.sidebar.number_input("Prix actuel de l'actif sous-jacent (S)", value=100.0, min_value=0.0)
K = st.sidebar.number_input("Prix d'exercice (K)", value=100.0, min_value=0.0)
r = st.sidebar.number_input("Taux sans risque annuel (r)", value=0.05, min_value=0.0)
sigma = st.sidebar.number_input("Volatilité annuelle (σ)", value=0.2, min_value=0.0)
T = st.sidebar.number_input("Temps restant jusqu'à l'échéance (T, en années)", value=1.0, min_value=0.0)

# Calcul des prix des options
call_price = black_scholes_call(S, K, r, sigma, T)
put_price = black_scholes_put(S, K, r, sigma, T)

# Afficher les résultats
st.subheader("Résultats")
st.write(f"Prix du Call : {call_price:.2f}")
st.write(f"Prix du Put : {put_price:.2f}")

# Visualisation des prix des options en fonction de S
st.subheader("Visualisation des prix des options")
S_values = np.linspace(50, 150, 100)
call_prices = [black_scholes_call(S_val, K, r, sigma, T) for S_val in S_values]
put_prices = [black_scholes_put(S_val, K, r, sigma, T) for S_val in S_values]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(S_values, call_prices, label="Call Price", color="blue")
ax.plot(S_values, put_prices, label="Put Price", color="red")
ax.axvline(K, linestyle="--", color="black", label="Strike Price")
ax.set_title("Prix des options en fonction du prix de l'actif sous-jacent")
ax.set_xlabel("Prix de l'actif sous-jacent (S)")
ax.set_ylabel("Prix de l'option")
ax.legend()
ax.grid()

st.pyplot(fig)

# Comparaison avec des données réelles
st.subheader("Comparaison avec des données réelles")
ticker = st.text_input("Symbol boursier (ex: AAPL)", value="AAPL")
expiration_date = st.text_input("Date d'échéance (YYYY-MM-DD)", value="2024-01-19")

if ticker and expiration_date:
    try:
        calls, puts = fetch_option_data(ticker, expiration_date)
        st.write("Options Call:")
        st.dataframe(calls[['strike', 'lastPrice']])
        st.write("Options Put:")
        st.dataframe(puts[['strike', 'lastPrice']])
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")

# Calcul des Greeks
def black_scholes_greeks(S, K, r, sigma, T):
    d1, d2 = calculate_d1_d2(S, K, r, sigma, T)
    delta_call = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta_call = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2)
    return {
        "Delta Call": delta_call,
        "Gamma": gamma,
        "Vega": vega,
        "Theta Call": theta_call,
        "Rho Call": rho_call
    }

greeks = black_scholes_greeks(S, K, r, sigma, T)
st.subheader("Greeks")
st.write(greeks)