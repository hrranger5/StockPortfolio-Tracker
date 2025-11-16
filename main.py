import csv
import sys

# 1. Hardcoded Stock Price Dictionary
# This dictionary simulates real-time stock prices for a simplified scope.
STOCK_PRICES = {
    "AAPL": 180.50,
    "GOOGL": 145.75,
    "MSFT": 410.25,
    "TSLA": 250.00,
    "AMZN": 175.90,
    "NVDA": 890.10,
    "JPM": 195.30
}

def get_user_holdings():
    """
    Prompts the user to input their stock holdings (ticker and quantity).

    Returns:
        dict: A dictionary where keys are stock tickers and values are quantities.
    """
    print("\n--- Enter Your Stock Holdings ---")
    holdings = {}

    while True:
        # Prompt for ticker symbol (or 'done' to stop)
        ticker = input(
            "Enter stock ticker (e.g., AAPL) or type 'done' to finish: "
        ).strip().upper()

        if ticker == 'DONE':
            break

        # Check if the ticker is in our defined prices
        if ticker not in STOCK_PRICES:
            print(f"Error: Stock '{ticker}' not found in the price list. Please try again.")
            continue

        # Prompt for quantity
        while True:
            try:
                quantity = int(input(f"Enter quantity for {ticker}: "))
                if quantity <= 0:
                    print("Quantity must be a positive whole number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a whole number for the quantity.")

        holdings[ticker] = quantity
        print(f"Added {quantity} shares of {ticker}.")

    return holdings

def calculate_portfolio_value(holdings):
    """
    Calculates the total value of the portfolio.

    Args:
        holdings (dict): User's stock holdings (ticker: quantity).

    Returns:
        tuple: (total_value, detailed_results)
               total_value (float): The grand total investment value.
               detailed_results (list): A list of dictionaries for each stock.
    """
    total_value = 0.0
    detailed_results = []

    print("\n--- Portfolio Valuation ---")

    for ticker, quantity in holdings.items():
        price = STOCK_PRICES.get(ticker) # Safely retrieve the price
        
        # This check is mostly for safety, as we already verified the ticker during input
        if price is not None:
            value = price * quantity
            total_value += value
            
            # Store results for display and optional saving
            detailed_results.append({
                "ticker": ticker,
                "quantity": quantity,
                "price": price,
                "value": value
            })

            # Display the result for the individual stock
            print(f"{ticker}: {quantity} shares @ ${price:.2f} = ${value:,.2f}")
        else:
            # Should not happen if input validation works correctly
            print(f"Warning: Could not find price for {ticker}. Skipping calculation.")


    return total_value, detailed_results

def save_to_csv(results, total_value):
    """
    Saves the detailed portfolio results to a CSV file.

    Args:
        results (list): List of dictionaries containing detailed stock data.
        total_value (float): The final calculated portfolio value.
    """
    filename = 'portfolio_summary.csv'
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write header
            writer.writerow(["Stock Ticker", "Quantity", "Price", "Value"])
            
            # Write individual stock data
            for item in results:
                writer.writerow([
                    item["ticker"],
                    item["quantity"],
                    f"{item['price']:.2f}",
                    f"{item['value']:,.2f}"
                ])
                
            # Add a summary line
            writer.writerow(["", "", "---", "---"])
            writer.writerow(["TOTAL PORTFOLIO VALUE", "", "", f"${total_value:,.2f}"])
        
        print(f"\n--- SUCCESS: Results saved to {filename} ---")
        
    except IOError as e:
        print(f"\n--- ERROR: Could not write to file {filename} ---")
        print(f"Details: {e}")


if __name__ == "__main__":
    
    # 1. Get Holdings
    user_holdings = get_user_holdings()
    
    if not user_holdings:
        print("No holdings entered. Exiting program.")
        sys.exit()

    # 2. Calculate Value
    final_value, detailed_data = calculate_portfolio_value(user_holdings)

    # 3. Display Final Result
    print("\n---------------------------------")
    print(f"TOTAL INVESTMENT VALUE: ${final_value:,.2f}")
    print("---------------------------------")

    # 4. Optional File Handling
    save_option = input("\nWould you like to save these results to a CSV file? (y/n): ").strip().lower()
    
    if save_option == 'y':
        save_to_csv(detailed_data, final_value)
    else:
        print("File saving skipped.")
    
    print("\nProgram finished. Have a great day!")
