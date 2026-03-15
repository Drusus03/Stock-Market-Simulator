# 📈 Stock Market Simulator

> A command-line stock market simulation built in Python.  
> Developed by [Tuza nav tak]

---

## 📋 Requirements

- Python 3.10 or higher
- matplotlib library

Check your Python version:
```bash
python3 --version
```

Install the required library:
```bash
python3 -m pip install matplotlib
```

> ⚠️ Always use `python3 -m pip install` on Windows — not just `pip install`.  
> This ensures the library installs into the correct Python version.

---

## 📁 Project Structure

```
stock_market_simulator/
├── main.py          → Entry point, menu system
├── market.py        → Stock prices, simulation, news events
├── trading.py       → Buy/sell logic
├── portfolio.py     → Portfolio tracking, saving, loading
├── history.py       → Trade history logging
├── bot.py           → Automated moving average trading bot
└── README.md        → This file
```

These files are auto-generated when you save:
```
portfolio.json       → Your saved balance and holdings
history.csv          → Your saved trade history
```

---

## 🚀 How to Run

```bash
# Step 1 — Go into the project folder
cd stock_market_simulator

# Step 2 — Run the program
python3 main.py
```

---

## 🎮 Menu Options

| Option | Action |
|--------|--------|
| 1  | View current stock market prices |
| 2  | Buy a stock |
| 3  | Sell a stock |
| 4  | View your portfolio and P&L |
| 5  | View full trade history |
| 6  | Advance to the next day |
| 7  | View price chart for one stock |
| 8  | View price chart for all stocks |
| 9  | View portfolio value over time |
| 10 | Run the automated trading bot |
| 11 | Save portfolio and trade history |
| 12 | Add balance to your account |
| 13 | Exit |

---

## 💾 Save System

Your data is automatically saved when you use **Option 11** or choose to save on exit.

- `portfolio.json` — stores your balance, holdings, and value history
- `history.csv` — stores every trade you've made

On the next run, your data loads automatically.  
To start fresh, delete both `portfolio.json` and `history.csv`.

---

## 🤖 Trading Bot

The bot uses a **Moving Average Crossover Strategy**:

- Short-term MA (5 days) vs Long-term MA (20 days)
- If MA5 > MA20 → BUY signal (uptrend)
- If MA5 < MA20 → SELL signal (downtrend)

> Requires at least 20 days of price history to generate signals.  
> Run **Option 6** (Next Day) at least 20 times before using the bot.

---

## 📰 Market News Events

Every day there is a 10% chance of a news event per stock:
- 5% chance of bad news → stock drops 5–15%
- 5% chance of good news → stock rises 5–15%

---

## 📊 Available Stocks

| Symbol | Company          | Starting Price |
|--------|------------------|----------------|
| AAPL   | Apple            | $175.00 |
| TSLA   | Tesla            | $210.00 |
| GOOG   | Google           | $140.00 |
| AMZN   | Amazon           | $185.00 |
| MSFT   | Microsoft        | $420.00 |

---

## ❌ Common Errors and Fixes

**ModuleNotFoundError: No module named 'matplotlib'**
```bash
python3 -m pip install matplotlib
```

**File not found / import errors**
```bash
# Make sure you are inside the project folder
cd stock_market_simulator
python3 main.py
```

**Emoji warning in graph title**
```
UserWarning: Glyph missing from font DejaVu Sans
```
This is harmless. The graph still works. It just means matplotlib  
cannot render emojis in plot titles — safe to ignore.

---

## 🧠 Concepts Demonstrated

- Modular programming (6 separate files)
- Stock market simulation using random walk model
- File handling (JSON save/load, CSV export)
- Data visualization using matplotlib
- Algorithmic trading (moving average strategy)
- Event-driven simulation (news events)
- Object-like state management using Python modules

---

## 📬 Contact

**Parth**  
DMCE — Artificial Intelligence & Data Science  
Semester 2 | 2025
