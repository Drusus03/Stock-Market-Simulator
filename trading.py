import market
import portfolio
import history

# ─────────────────────────────────────────────
# FUNCTION: Buy stock
# ─────────────────────────────────────────────
def buy_stock(symbol, quantity):
    """
    Buys 'quantity' shares of 'symbol'.
    
    Steps:
    1. Validate the stock symbol exists
    2. Check if user has enough cash
    3. Deduct cash from balance
    4. Add shares to holdings
    5. Update average buy price
    6. Log the trade
    """
    symbol = symbol.upper()

    # --- Validate stock exists ---
    price = market.get_price(symbol)
    if price is None:
        print(f"  ❌ Stock '{symbol}' not found.")
        return

    # --- Validate quantity ---
    if quantity <= 0:
        print("  ❌ Quantity must be greater than 0.")
        return

    # --- Check funds ---
    total_cost = round(price * quantity, 2)
    if total_cost > portfolio.balance:
        print(f"  ❌ Insufficient funds.")
        print(f"     Need: ${total_cost:.2f} | Have: ${portfolio.balance:.2f}")
        return

    # --- Deduct balance ---
    portfolio.balance -= total_cost
    portfolio.balance = round(portfolio.balance, 2)

    # --- Update holdings with weighted average buy price ---
    if symbol in portfolio.holdings:
        existing = portfolio.holdings[symbol]
        old_shares = existing["shares"]
        old_avg    = existing["avg_buy"]
        new_shares = old_shares + quantity

        # Weighted average formula:
        # new_avg = (old_shares * old_avg + quantity * price) / new_shares
        new_avg = ((old_shares * old_avg) + (quantity * price)) / new_shares

        portfolio.holdings[symbol]["shares"]  = new_shares
        portfolio.holdings[symbol]["avg_buy"] = round(new_avg, 4)
    else:
        portfolio.holdings[symbol] = {
            "shares":  quantity,
            "avg_buy": price
        }

    # --- Log trade ---
    history.record_trade("BUY", symbol, quantity, price, market.current_day)

    print(f"  ✅ Bought {quantity} share(s) of {symbol} at ${price:.2f}")
    print(f"  💵 Spent: ${total_cost:.2f} | Remaining: ${portfolio.balance:.2f}")


# ─────────────────────────────────────────────
# FUNCTION: Sell stock
# ─────────────────────────────────────────────
def sell_stock(symbol, quantity):
    """
    Sells 'quantity' shares of 'symbol'.
    
    Steps:
    1. Validate symbol and ownership
    2. Check user owns enough shares
    3. Add proceeds to balance
    4. Reduce shares in holdings
    5. Remove stock if 0 shares remain
    6. Log the trade
    """
    symbol = symbol.upper()

    # --- Check ownership ---
    if symbol not in portfolio.holdings:
        print(f"  ❌ You don't own any {symbol} stock.")
        return

    owned = portfolio.holdings[symbol]["shares"]
    if quantity <= 0:
        print("  ❌ Quantity must be greater than 0.")
        return
    if quantity > owned:
        print(f"  ❌ You only own {owned} share(s) of {symbol}.")
        return

    # --- Get current price ---
    price = market.get_price(symbol)
    proceeds = round(price * quantity, 2)

    # --- Add proceeds to balance ---
    portfolio.balance += proceeds
    portfolio.balance = round(portfolio.balance, 2)

    # --- Update holdings ---
    portfolio.holdings[symbol]["shares"] -= quantity
    if portfolio.holdings[symbol]["shares"] == 0:
        del portfolio.holdings[symbol]  # Remove if no shares left

    # --- Log trade ---
    history.record_trade("SELL", symbol, quantity, price, market.current_day)

    print(f"  ✅ Sold {quantity} share(s) of {symbol} at ${price:.2f}")
    print(f"  💵 Received: ${proceeds:.2f} | Balance: ${portfolio.balance:.2f}")