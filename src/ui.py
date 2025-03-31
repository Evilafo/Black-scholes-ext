import ipywidgets as widgets
from IPython.display import display
from black_scholes import black_scholes_call, black_scholes_put

def update_prices(S, K, r, sigma, T):
    """Met à jour les prix des options en fonction des paramètres."""
    call_price = black_scholes_call(S, K, r, sigma, T)
    put_price = black_scholes_put(S, K, r, sigma, T)
    print(f"Prix du call : {call_price:.2f}")
    print(f"Prix du put : {put_price:.2f}")

# Widgets pour l'interface utilisateur
S_widget = widgets.FloatSlider(value=100, min=50, max=150, step=1, description="Prix actuel (S)")
K_widget = widgets.FloatSlider(value=100, min=50, max=150, step=1, description="Strike (K)")
r_widget = widgets.FloatSlider(value=0.05, min=0, max=0.1, step=0.01, description="Taux (r)")
sigma_widget = widgets.FloatSlider(value=0.2, min=0.1, max=0.5, step=0.01, description="Volatilité (σ)")
T_widget = widgets.FloatSlider(value=1, min=0.1, max=2, step=0.1, description="Temps (T)")

# Lier les widgets à la fonction
widgets.interactive(update_prices, S=S_widget, K=K_widget, r=r_widget, sigma=sigma_widget, T=T_widget)