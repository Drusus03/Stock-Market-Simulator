import random

# ─────────────────────────────────────────────
# STOCK UNIVERSE
# Each stock has: current price, history list
# ─────────────────────────────────────────────
STOCKS = {
    "AAPL": {"price": 175.0,  "history": [175.0]},
    "TSLA": {"price": 210.0,  "history": [210.0]},
    "GOOG": {"price": 140.0,  "history": [140.0]},
    "AMZN": {"price": 185.0,  "history": [185.0]},
    "MSFT": {"price": 420.0,  "history": [420.0]},
}

# Track which day we're on
current_day = 1

# ─────────────────────────────────────────────
# FUNCTION: Get current price of a stock
# ─────────────────────────────────────────────
def get_price(symbol):
    """Returns the current price of a stock by its symbol."""
    if symbol in STOCKS:
        return STOCKS[symbol]["price"]
    return None

# ─────────────────────────────────────────────
# FUNCTION: Get full price history of a stock
# ─────────────────────────────────────────────
def get_history(symbol):
    """Returns list of all past prices for a stock."""
    if symbol in STOCKS:
        return STOCKS[symbol]["history"]
    return []

# ─────────────────────────────────────────────
# FUNCTION: Display the market (all stock prices)
# ─────────────────────────────────────────────
def display_market():
    """Prints all stock prices in a formatted table."""
    print("\n" + "="*50)
    print(f"  📈  STOCK MARKET  —  Day {current_day}")
    print("="*50)
    print(f"  {'SYMBOL':<8} {'PRICE':>10}  {'CHANGE':>10}")
    print("-"*50)
    for symbol, data in STOCKS.items():
        price = data["price"]
        history = data["history"]
        # Calculate change from previous day
        if len(history) > 1:
            prev = history[-2]
            change = price - prev
            change_pct = (change / prev) * 100
            arrow = "▲" if change >= 0 else "▼"
            print(f"  {symbol:<8} ${price:>9.2f}  {arrow} {change_pct:+.2f}%")
        else:
            print(f"  {symbol:<8} ${price:>9.2f}  {'—':>10}")
    print("="*50)

# ─────────────────────────────────────────────
# FUNCTION: Simulate one day passing
# Returns list of news events that happened
# ─────────────────────────────────────────────
def next_day():
    """
    Advances the market by one day.
    - Prices change randomly (random walk model)
    - 10% chance of a news event per stock
    Returns a list of news strings.
    """
    global current_day
    current_day += 1
    news_events = []

    for symbol, data in STOCKS.items():
        price = data["price"]

        # --- UPGRADE 2: Market News Events ---
        # 10% chance something newsworthy happens
        news_roll = random.random()  # 0.0 to 1.0

        if news_roll < 0.05:
            # BAD NEWS: big drop (5% to 15%)
            shock = random.uniform(-0.15, -0.05)
            news_events.append(
                f"🔴 BAD NEWS: {symbol} — "
                f"{random.choice(NEGATIVE_HEADLINES[symbol])} "
                f"(Stock dropped {abs(shock)*100:.1f}%)"
            )
        elif news_roll < 0.10:
            # GOOD NEWS: big rise (5% to 15%)
            shock = random.uniform(0.05, 0.15)
            news_events.append(
                f"🟢 GOOD NEWS: {symbol} — "
                f"{random.choice(POSITIVE_HEADLINES[symbol])} "
                f"(Stock rose {shock*100:.1f}%)"
            )
        else:
            # Normal day: small random movement
            # drift = small upward bias, volatility = randomness
            drift = 0.001
            volatility = 0.02
            shock = drift + volatility * random.gauss(0, 1)

        # Apply the price change
        new_price = round(price * (1 + shock), 2)
        # Price can't go below $1
        new_price = max(new_price, 1.0)

        STOCKS[symbol]["price"] = new_price
        STOCKS[symbol]["history"].append(new_price)

    return news_events

# ─────────────────────────────────────────────
# UPGRADE 2: News Headlines per stock
# ─────────────────────────────────────────────
POSITIVE_HEADLINES = {
    "AAPL": ["iPhone sales surge!", "Apple announces new AI chip.", "Record quarterly earnings."],
    "TSLA": ["Tesla gigafactory opens.", "Record deliveries this quarter.", "New model revealed."],
    "GOOG": ["Google wins antitrust case.", "Search revenue beats estimates.", "AI assistant launches."],
    "AMZN": ["Amazon Prime hits 300M users.", "AWS cloud revenue explodes.", "Record holiday sales."],
    "MSFT": ["Azure growth beats rivals.", "Copilot adoption soaring.", "Record cloud revenue."],
}

NEGATIVE_HEADLINES = {
    "AAPL": ["iPhone sales disappoint.", "Supply chain crisis hits.", "Regulatory probe launched."],
    "TSLA": ["Recall issued for 50K vehicles.", "Elon sells more stock.", "Delivery miss reported."],
    "GOOG": ["Antitrust fine issued.", "Ad revenue slows down.", "Data breach reported."],
    "AMZN": ["Union strike disrupts ops.", "AWS outage reported.", "Earnings miss estimates."],
    "MSFT": ["Security vulnerability found.", "Layoffs announced.", "Cloud growth slows."],
}

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plot_stock(symbol):
    """
    Plots the price history of a single stock.
    Shows a line chart with day numbers on X-axis.
    """
    symbol = symbol.upper()
    if symbol not in STOCKS:
        print(f"  ❌ Stock '{symbol}' not found.")
        return

    prices = STOCKS[symbol]["history"]
    days   = list(range(1, len(prices) + 1))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(days, prices, color="#00bfff", linewidth=2, marker="o", markersize=3)
    ax.fill_between(days, prices, alpha=0.1, color="#00bfff")
    ax.set_title(f"{symbol} — Price History", fontsize=14, fontweight="bold")
    ax.set_xlabel("Day")
    ax.set_ylabel("Price ($)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_all_stocks():
    """
    Plots all stocks in a 2x3 grid layout.
    """
    symbols = list(STOCKS.keys())
    colors  = ["#00bfff", "#ff6b6b", "#51cf66", "#ffd43b", "#cc5de8"]

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle("Stock Market — All Prices", fontsize=16, fontweight="bold")

    for i, symbol in enumerate(symbols):
        row = i // 3
        col = i % 3
        ax  = axes[row][col]
        prices = STOCKS[symbol]["history"]
        days   = list(range(1, len(prices) + 1))
        ax.plot(days, prices, color=colors[i], linewidth=2)
        ax.fill_between(days, prices, alpha=0.15, color=colors[i])
        ax.set_title(symbol, fontweight="bold")
        ax.set_xlabel("Day")
        ax.set_ylabel("$")
        ax.grid(True, alpha=0.3)

    # Hide the empty 6th subplot (we only have 5 stocks)
    axes[1][2].set_visible(False)
    plt.tight_layout()
    plt.show()