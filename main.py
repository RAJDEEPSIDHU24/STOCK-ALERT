from stocks import StockChangeRecognizer
from datetime import datetime
import os
COMPANIES = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "WIPRO.NS", "ITC.NS",
    "HCLTECH.NS", "AXISBANK.NS", "KOTAKBANK.NS", "TATAMOTORS.NS", "MARUTI.NS"
]

COMPANY_NAMES = [
    "Reliance Industries", "TCS", "Infosys", "HDFC Bank", "ICICI Bank",
    "Hindustan Unilever", "SBI", "Bharti Airtel", "Wipro", "ITC",
    "HCL Technologies", "Axis Bank", "Kotak Mahindra Bank", "Tata Motors", "Maruti Suzuki"
]

def get_user_dates():
    print("\n📅 Enter date range (press Enter to use last 7 days)")
    from_date = input("From Date (YYYY-MM-DD): ") or (datetime.today().strftime('%Y-%m-%d'))
    to_date = input("To Date (YYYY-MM-DD): ") or (datetime.today().strftime('%Y-%m-%d'))
    return from_date, to_date

def save_report_to_file(content: str):
    with open("stock_report.txt", "a", encoding="utf-8") as file:
        file.write(content + "\n\n")

if __name__ == "__main__":
    print("📊 Top 15 Indian Companies")
    for i, name in enumerate(COMPANY_NAMES, 1):
        print(f"{i}. {name}")

    while True:
        try:
            choice = int(input("\n🔢 Enter the number of the company to check stock: "))
            if 1 <= choice <= 15:
                stock_symbol = COMPANIES[choice - 1]
                stock_name = COMPANY_NAMES[choice - 1]

                from_date, to_date = get_user_dates()
                print(f"\n🔍 Analyzing {stock_name} from {from_date} to {to_date}...")

                recognizer = StockChangeRecognizer(stock_name, stock_symbol, from_date, to_date)
                recognizer.get_data_and_analyze()

                message = recognizer.get_message()
                print("\n" + message)

                save_report_to_file(message)
            else:
                print("❗ Invalid selection. Choose a number from 1 to 15.")
        except ValueError:
            print("❗ Please enter a valid number.")

        again = input("\n🔁 Do you want to check another company? (y/n): ").lower()
        if again != "y":
            print("\n✅ Thank you for using Indian Stock CLI Tracker!")
            break

