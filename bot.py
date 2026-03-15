import market
import trading
import portfolio

# ─────────────────────────────────────────────
# FUNCTION: Calculate moving average
# ─────────────────────────────────────────────
def moving_average(prices, window):
    """
    Returns the average of the last 'window' prices.
    If not enough data, returns None.
    
    Example:
        prices = [100, 102, 98, 105, 103]
        window = 3
        → average of [98, 105, 103] = 102.0
    """
    if len(prices) < window:
        return None  # Not enough data yet
    return sum(prices[-window:]) / window

# ─────────────────────────────────────────────
# FUNCTION: Run the bot for one day
# ─────────────────────────────────────────────
def run_bot(short_window=5, long_window=20, shares_per_trade=2):
    """
    Scans all stocks and makes trades based on moving average crossover.
    
    short_window → fast-moving average (default: 5 days)
    long_window  → slow-moving average (default: 20 days)
    shares_per_trade → how many shares to buy/sell per signal
    """
    print("\n" + "="*55)
    print("  🤖  TRADING BOT ANALYSIS")
    print("="*55)

    any_action = False

    for symbol in market.STOCKS:
        prices   = market.get_history(symbol)
        price    = market.get_price(symbol)
        ma_short = moving_average(prices, short_window)
        ma_long  = moving_average(prices, long_window)

        print(f"\n  {symbol}")

        # Not enough data to decide
        if ma_short is None or ma_long is None:
            days_needed = long_window - len(prices)
            print(f"    📊 Need {days_needed} more day(s) of data for signal.")
            continue

        print(f"    MA{short_window}  = ${ma_short:.2f}")
        print(f"    MA{long_window} = ${ma_long:.2f}")

        if ma_short > ma_long:
            # BULLISH SIGNAL → BUY
            print(f"    🟢 SIGNAL: BUY — Short MA above Long MA (uptrend)")
            # Only buy if we can afford it
            if portfolio.balance >= price * shares_per_trade:
                trading.buy_stock(symbol, shares_per_trade)
                any_action = True
            else:
                print(f"    ⚠️  Not enough funds to buy.")

        elif ma_short < ma_long:
            # BEARISH SIGNAL → SELL
            print(f"    🔴 SIGNAL: SELL — Short MA below Long MA (downtrend)")
            # Only sell if we own shares
            owned = portfolio.holdings.get(symbol, {}).get("shares", 0)
            if owned >= shares_per_trade:
                trading.sell_stock(symbol, shares_per_trade)
                any_action = True
            elif owned > 0:
                trading.sell_stock(symbol, owned)  # Sell whatever we have
                any_action = True
            else:
                print(f"    ⚠️  No shares to sell.")
        else:
            print(f"    ⬜ SIGNAL: HOLD — MAs are equal.")

    if not any_action:
        print("\n  Bot made no trades this cycle.")
    print("="*55)