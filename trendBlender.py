import requests
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time
import oracledb
import getpass
import traceback
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


user = 'admin'
cs = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.us-sanjose-1.oraclecloud.com))(connect_data=(service_name=g487fd57cfa0268_trendblender_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'

pw = getpass.getpass("Enter password: ")

def trendblender_run():
    req = requests.get("https://www.investing.com/currencies/gbp-usd")
    soup = BeautifulSoup(req.content, "html.parser")

    price_element = soup.find('div', {'class': 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]', 'data-test': 'instrument-price-last'})

    if price_element:
        price = price_element.text.strip()
        now = datetime.now()
        pt_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            connection = oracledb.connect(user=user, password=pw, dsn=cs)

            with connection.cursor() as cursor:
                
                sqlin = "INSERT INTO price_tracker (domain_timestamp, pair, value) VALUES (TO_DATE(:1, 'YYYY-MM-DD HH24:MI:SS'), :2, :3)"
                cursor.execute(sqlin, (pt_timestamp, 'GBP/USD', price))
                connection.commit()
                print("Table updated successfully.")

                sqlret = "SELECT TO_CHAR(domain_timestamp, 'YYYY-MM-DD HH24:MI:SS') AS timestamp, value FROM price_tracker"
                cursor.execute(sqlret)

                rows = cursor.fetchall()

                timestamps = []
                values = []

                for row in rows:
                    timestamps.append(row[0])
                    values.append(row[1])

                print("Timestamps: " + str(timestamps))
                print("Values: " + str(values))

                plt.figure(figsize=(10, 6))
                plt.plot(timestamps, values, marker='o', linestyle='-', color='b')
                plt.title('GBP/USD Price Over Time')
                plt.xlabel('Timestamp')
                plt.ylabel('Price')
                plt.xticks(rotation=45)
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
                plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
                plt.gcf().autofmt_xdate()  
                plt.tight_layout()
                plt.show()
                

        except oracledb.Error as e:
            error, = e.args
            print(error.message)
            traceback.print_tb(e.__traceback__)

        finally:
            connection.close()

        print(pt_timestamp + " " + price)
    else:
        print("Price element not found.")

schedule.every().minute.do(trendblender_run)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user.")
