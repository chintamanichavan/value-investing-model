# value-investing-model

A simple discounted-cash-flow (DCF) intrinsic-value calculator. Fetches stock cash flows via `yfinance`, projects them, applies a terminal-value perpetuity-growth model, and reports intrinsic value.

## Run

```
pip install yfinance numpy matplotlib
python value_investing.py
```

Edit the ticker and parameters (`discount_rate`, `growth_rate`, `projection_years`) inline.

## Status

Single-file experiment from a value-investing reading group. Not investment advice.
