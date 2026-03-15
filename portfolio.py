import market
import history

# ─────────────────────────────────────────────
# PORTFOLIO STATE
# holdings = { "AAPL": {"shares": 5, "avg_buy": 170.0}, ... }
# balance  = cash available
# value_history = portfolio total value over time
# ─────────────────────────────────────────────
balance = 10000.0          # Starting cash
holdings = {}              # Stocks owned
value_history = [10000.0]  # Track value over time (Upgrade 1)

# ─────────────────────────────────────────────
# FUNCTION: Get total portfolio value
# ─────────────────────────────────────────────
def get_total_value():
    """
    Returns total worth = cash + value of all stocks owned.
    """
    stock_value = 0
    for symbol, data in holdings.items():
        current_price = market.get_price(symbol)
        stock_value += data["shares"] * current_price
    return round(balance + stock_value, 2)

# ─────────────────────────────────────────────
# FUNCTION: Snapshot portfolio value (called each day)
# ─────────────────────────────────────────────
def snapshot_value():
    """Records current portfolio value into value_history."""
    value_history.append(get_total_value())

# ─────────────────────────────────────────────
# FUNCTION: Display portfolio
# ─────────────────────────────────────────────
def display_portfolio():
    """Shows balance, holdings, P&L for each stock."""
    total = get_total_value()
    profit_loss = total - 10000.0  # vs starting balance

    print("\n" + "="*65)
    print("  💼  YOUR PORTFOLIO")
    print("="*65)
    print(f"  💵 Cash Balance  : ${balance:,.2f}")
    print(f"  📊 Total Value   : ${total:,.2f}")

    if profit_loss >= 0:
        print(f"  📈 Total P&L     : +${profit_loss:,.2f} 🟢")
    else:
        print(f"  📉 Total P&L     : -${abs(profit_loss):,.2f} 🔴")

    print("-"*65)

    if not holdings:
        print("  No stocks owned yet.")
    else:
        print(f"  {'STOCK':<8} {'SHARES':>7} {'AVG BUY':>10} {'NOW':>10} {'P&L':>12}")
        print("-"*65)
        for symbol, data in holdings.items():
            shares    = data["shares"]
            avg_buy   = data["avg_buy"]
            now       = market.get_price(symbol)
            pl        = (now - avg_buy) * shares
            pl_str    = f"+${pl:.2f}" if pl >= 0 else f"-${abs(pl):.2f}"
            icon      = "🟢" if pl >= 0 else "🔴"
            print(
                f"  {symbol:<8} {shares:>7} "
                f"${avg_buy:>9.2f} "
                f"${now:>9.2f} "
                f"{icon}{pl_str:>10}"
            )

    print("="*65)

# ─────────────────────────────────────────────
# FUNCTION: Save portfolio to text file
# ─────────────────────────────────────────────
import json

SAVE_FILE = "portfolio.json"

def save_portfolio():
    data = {
        "balance":       balance,
        "holdings":      holdings,
        "value_history": value_history,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    history.save_history()
    print("  ✅ Portfolio saved to portfolio.json")
    print("  ✅ Trade history saved to history.csv")

def load_portfolio():
    global balance, holdings, value_history
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        balance       = data.get("balance",       10000.0)
        holdings      = data.get("holdings",      {})
        value_history = data.get("value_history", [balance])
        print(f"  ✅ Portfolio loaded. Balance: ${balance:,.2f}")
    except FileNotFoundError:
        print("  ℹ️  No save file found. Starting fresh.")
    except json.JSONDecodeError:
        print("  ⚠️  Save file corrupted. Starting fresh.")

def load_history():
    import csv
    try:
        with open("history.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                history.trade_log.append({
                    "time":     row["time"],
                    "day":      int(row["day"]),
                    "action":   row["action"],
                    "symbol":   row["symbol"],
                    "quantity": int(row["quantity"]),
                    "price":    float(row["price"]),
                    "total":    float(row["total"]),
                })
        print(f"  ✅ Trade history loaded.")
    except FileNotFoundError:
        pass
# Add this to portfolio.py (bottom of file)

import matplotlib.pyplot as plt

def plot_portfolio_value():
    """
    UPGRADE 1: Plots total portfolio value over time.
    Shows how your net worth has changed day by day.
    """
    if len(value_history) < 2:
        print("  ⚠️  Need at least 2 days of data to plot.")
        return

    days   = list(range(1, len(value_history) + 1))
    values = value_history
    start  = values[0]

    # Color based on performance
    final_color = "#51cf66" if values[-1] >= start else "#ff6b6b"

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(days, values, color=final_color, linewidth=2.5, marker="o", markersize=4)
    ax.fill_between(days, values, start, alpha=0.15, color=final_color)
    ax.axhline(y=start, color="gray", linestyle="--", alpha=0.7, label=f"Start: ${start:,.0f}")
    ax.set_title("📊 Portfolio Value Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Day")
    ax.set_ylabel("Total Value ($)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def add_balance(amount):
    global balance
    if amount <= 0:
        print("  ❌ Amount must be greater than 0.")
        return
    balance += amount
    balance = round(balance, 2)
    print(f"  ✅ Added ${amount:,.2f} to your account.")
    print(f"  💵 New Balance: ${balance:,.2f}")