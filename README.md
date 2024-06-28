TrendBlender.py : GBP/USD Currency Pair Price Tracker and Visualization
TrendBlender is a Python script designed to fetch real-time GBP/USD currency pair prices from a financial website, store them in an Oracle database, and visualize historical price trends using Matplotlib.

Features
Web Scraping: Utilizes requests and BeautifulSoup to fetch current GBP/USD price data from "https://www.investing.com/currencies/gbp-usd".
Database Interaction: Inserts fetched data into an Oracle database (price_tracker) with timestamp, currency pair, and price columns.
Data Visualization: Plots historical GBP/USD prices over time using Matplotlib, including markers, labels, and formatted timestamps.
Periodic Updates: Automates data fetching and visualization at regular intervals using schedule.
Installation

Clone the repository:

bash
Copy code
git clone https://github.com/your-username/trendblender.git
cd trendblender

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure Oracle Database:

Update user, pw, and cs variables in the script with your Oracle database credentials.
Usage


Run the script to start tracking and visualizing GBP/USD prices:

bash
Copy code
python trendblender.py
The script will fetch real-time data every minute, store it in the database, and update the visualization accordingly.

Requirements
Python 3.x
requests, beautifulsoup4, matplotlib, schedule, oracledb Python packages
Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

License
This project is licensed under the MIT License - see the LICENSE file for details.

