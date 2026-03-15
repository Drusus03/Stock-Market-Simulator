# ─────────────────────────────────────────────
# Project  : Stock Market Simulator
# Author   : Parth Mahadeo Korgaonkar
# College  : DMCE — AI-DS, Sem 2
# Year     : 2025
# File     : main.py
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# STOCK MARKET SIMULATOR
# Entry point — main menu and game loop
# ─────────────────────────────────────────────

import market
import trading
import portfolio
import history
import bot

# ─────────────────────────────────────────────
# HELPER: Clear-looking separator
# ─────────────────────────────────────────────
def separator():
    print("\n" + "─"*55)

# ─────────────────────────────────────────────
# FUNCTION: Print main menu
# ─────────────────────────────────────────────
def print_menu():
    print("\n╔══════════════════════════════════════╗")
    print("║    📈  STOCK MARKET SIMULATOR         ║")
    print(f"║    Day: {market.current_day:<4}  Balance: ${portfolio.balance:>9,.2f}  ║")
    print("╠══════════════════════════════════════╣")
    print("║  1  View Market                      ║")
    print("║  2  Buy Stock                        ║")
    print("║  3  Sell Stock                       ║")
    print("║  4  Portfolio                        ║")
    print("║  5  Trade History                    ║")
    print("║  6  Next Day ⏭️                       ║")
    print("║  7  Stock Chart 📊                   ║")
    print("║  8  All Stocks Chart 📉               ║")
    print("║  9  Portfolio Graph 💹               ║")
    print("║  10 Run Trading Bot 🤖               ║")
    print("║  11 Save Portfolio 💾                ║")
    print("║  12 Add Balance 💰               ║")
    print("║  13 Exit ❌                      ║")
    print("╚══════════════════════════════════════╝")

# ─────────────────────────────────────────────
# FUNCTION: Get a valid integer input
# ─────────────────────────────────────────────
def get_int(prompt, min_val=1):
    """Keeps asking until user enters a valid integer >= min_val."""
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"  ❌ Enter a number >= {min_val}")
                continue
            return val
        except ValueError:
            print("  ❌ Please enter a whole number.")

# ─────────────────────────────────────────────
# FUNCTION: Handle 'Next Day'
# ─────────────────────────────────────────────
def advance_day():
    """
    Moves to the next market day:
    1. Simulate price changes
    2. Show any news events
    3. Record portfolio value snapshot
    """
    print(f"\n  ⏭️  Advancing to Day {market.current_day + 1}...")
    news = market.next_day()
    portfolio.snapshot_value()

    if news:
        separator()
        print("  📰  MARKET NEWS")
        separator()
        for item in news:
            print(f"  {item}")
    else:
        print("  📰 No major news today.")

    separator()
    print(f"  ✅ It is now Day {market.current_day}")

# ─────────────────────────────────────────────
# FUNCTION: Buy flow
# ─────────────────────────────────────────────
def buy_flow():
    market.display_market()
    symbol   = input("\n  Enter stock symbol: ").strip().upper()
    quantity = get_int("  Enter quantity to buy: ")
    trading.buy_stock(symbol, quantity)

# ─────────────────────────────────────────────
# FUNCTION: Sell flow
# ─────────────────────────────────────────────
def sell_flow():
    portfolio.display_portfolio()
    symbol   = input("\n  Enter stock symbol to sell: ").strip().upper()
    quantity = get_int("  Enter quantity to sell: ")
    trading.sell_stock(symbol, quantity)

# ─────────────────────────────────────────────
# FUNCTION: Stock chart flow
# ─────────────────────────────────────────────
def chart_flow():
    market.display_market()
    symbol = input("\n  Enter stock symbol to chart: ").strip().upper()
    market.plot_stock(symbol)

# ─────────────────────────────────────────────
# MAIN GAME LOOP
# ─────────────────────────────────────────────
def main():
    portfolio.load_portfolio()  
    portfolio.load_history()  

    print("\n  Welcome to the Stock Market Simulator!")
    print(f"  Starting balance: ${portfolio.balance:,.2f}")
    print("  Try to grow your portfolio. Good luck!\n")

    while True:
        print_menu()
        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            market.display_market()

        elif choice == "2":
            buy_flow()

        elif choice == "3":
            sell_flow()

        elif choice == "4":
            portfolio.display_portfolio()

        elif choice == "5":
            history.display_history()

        elif choice == "6":
            advance_day()

        elif choice == "7":
            chart_flow()

        elif choice == "8":
            market.plot_all_stocks()

        elif choice == "9":
            portfolio.plot_portfolio_value()

        elif choice == "10":
            bot.run_bot()

        elif choice == "11":
            portfolio.save_portfolio()

        elif choice == "12":
            try:
                amount = float(input("  Enter amount to add: $"))
                portfolio.add_balance(amount)
            except ValueError:
                print("  ❌ Enter a valid number.")

        elif choice == "13":
            print("\n  👋 Thanks for trading. Final portfolio value: "
                  f"${portfolio.get_total_value():,.2f}")
            save = input("  Save before exiting? (y/n): ").strip().lower()
            if save == "y":
                portfolio.save_portfolio()
            print("  Goodbye!\n")
            break

        else:
            print("  ❌ Invalid choice. Enter 1–12.")

# ─────────────────────────────────────────────
# Run the program
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()

# ─────────────────────────────────────────────
# Project  : Stock Market Simulator
# Author   : Parth Mahadeo Korgaonkar
# College  : DMCE — AI-DS, Sem 2
# Year     : 2025
# File     : main.py
# ─────────────────────────────────────────────