#!/usr/bin/env python3

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5y")
    return hist

def calculate_intrinsic_value(ticker, discount_rate=0.10, growth_rate=0.02, projection_years=5):
    stock = yf.Ticker(ticker)
    cash_flows = stock.cashflow
    projected_cash_flows = cash_flows.iloc[:, 0].values[:projection_years]  # Get the most recent cash flows

    # Debug: Print cash flows being used
    print(f"Projected Cash Flows: {projected_cash_flows}")

    # Calculate the terminal value using perpetuity growth model
    terminal_value = projected_cash_flows[-1] * (1 + growth_rate) / (discount_rate - growth_rate)
    
    # Debug: Print terminal value
    print(f"Terminal Value: {terminal_value}")

    # Discount the projected cash flows and terminal value to present value
    intrinsic_value = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(projected_cash_flows, start=1))
    intrinsic_value += terminal_value / (1 + discount_rate)**projection_years
    
    return intrinsic_value

def calculate_graham_number(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials
    balance_sheet = stock.balance_sheet

    # Checking for the available keys
    print("Available balance sheet keys:", balance_sheet.index)
    
    # Calculate EPS
    net_income = financials.loc['Net Income'].values[0]
    shares_outstanding = stock.info['sharesOutstanding']
    eps = net_income / shares_outstanding

    # Calculate BVPS
    total_assets = balance_sheet.loc['Total Assets'].values[0]
    
    # Handle potential discrepancies in key names
    try:
        total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].values[0]
    except KeyError:
        try:
            total_liabilities = balance_sheet.loc['Total Liabilities'].values[0]
        except KeyError:
            print("Could not find the total liabilities key.")
            return None

    book_value = total_assets - total_liabilities
    bvps = book_value / shares_outstanding

    # Calculate Graham Number
    graham_number = np.sqrt(22.5 * eps * bvps)
    return graham_number

def get_current_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period='1d')['Close'].iloc[0]

def main():
    ticker = input("Enter stock ticker: ").upper()
    data = get_stock_data(ticker)
    print(data)
    
    discount_rate = float(input("Enter discount rate (e.g., 0.10 for 10%): "))
    growth_rate = float(input("Enter growth rate (e.g., 0.02 for 2%): "))
    projection_years = int(input("Enter number of projection years: "))
    
    intrinsic_value = calculate_intrinsic_value(ticker, discount_rate, growth_rate, projection_years)
    print(f"\nThe intrinsic value of {ticker} based on DCF is approximately ${intrinsic_value:.2f}")
    
    graham_number = calculate_graham_number(ticker)
    if graham_number is not None:
        print(f"The Graham Number for {ticker} is approximately ${graham_number:.2f}")

    current_price = get_current_stock_price(ticker)
    print(f"The current stock price of {ticker} is ${current_price:.2f}")

    # Determine recommendation based on Graham Number
    if current_price < graham_number * 0.75:
        recommendation = "BUY"
    elif current_price > graham_number * 1.25:
        recommendation = "DO NOT BUY"
    else:
        recommendation = "HOLD OFF"

    print(f"Recommendation based on Graham Number if you don't own the stock: {recommendation}")

    # Visualization
    values = [intrinsic_value, graham_number, current_price]
    labels = ['Intrinsic Value', 'Graham Number', 'Current Price']
    plt.bar(labels, values, color=['blue', 'green', 'red'])
    plt.title(f"Intrinsic Value vs Graham Number vs Current Price for {ticker}")
    plt.ylabel('Value (USD)')
    plt.show()

if __name__ == "__main__":
    main()
