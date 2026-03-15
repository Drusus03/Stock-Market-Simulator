import csv
from datetime import datetime

# ─────────────────────────────────────────────
# In-memory list of all trades
# Each trade is a dictionary
# ─────────────────────────────────────────────
trade_log = []

# ─────────────────────────────────────────────
# FUNCTION: Record a new trade
# ─────────────────────────────────────────────
def record_trade(action, symbol, quantity, price, day):
    """
    Logs a trade to the in-memory trade log.
    
    action   → "BUY" or "SELL"
    symbol   → e.g. "AAPL"
    quantity → number of shares
    price    → price per share at time of trade
    day      → market day number
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    trade = {
        "time":     timestamp,
        "day":      day,
        "action":   action,
        "symbol":   symbol,
        "quantity": quantity,
        "price":    price,
        "total":    round(quantity * price, 2),
    }
    trade_log.append(trade)

# ─────────────────────────────────────────────
# FUNCTION: Display trade history
# ─────────────────────────────────────────────
def display_history():
    """Prints all trades in a formatted table."""
    if not trade_log:
        print("\n  No trades made yet.")
        return

    print("\n" + "="*65)
    print("  📋  TRADE HISTORY")
    print("="*65)
    print(f"  {'TIME':<10} {'DAY':<5} {'ACTION':<6} {'SYMBOL':<6} {'QTY':>5} {'PRICE':>10} {'TOTAL':>12}")
    print("-"*65)
    for t in trade_log:
        action_color = "🟢" if t["action"] == "BUY" else "🔴"
        print(
            f"  {t['time']:<10} "
            f"D{t['day']:<4} "
            f"{action_color}{t['action']:<5} "
            f"{t['symbol']:<6} "
            f"{t['quantity']:>5} "
            f"${t['price']:>9.2f} "
            f"${t['total']:>11.2f}"
        )
    print("="*65)

# ─────────────────────────────────────────────
# FUNCTION: Save trade history to CSV file
# ─────────────────────────────────────────────
def save_history(filename="history.csv"):
    """
    Saves all trades to a CSV file.
    CSV = Comma Separated Values — opens in Excel.
    """
    if not trade_log:
        print("  No trades to save.")
        return

    with open(filename, "w", newline="") as f:
        # Define column headers
        fieldnames = ["time", "day", "action", "symbol", "quantity", "price", "total"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()       # Write the header row
        writer.writerows(trade_log) # Write all trade rows

    print(f"  ✅ Trade history saved to {filename}")