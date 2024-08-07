# Financial app

import sqlite3
import re
import matplotlib.pyplot as plt
import pandas as pd
from colorama import init, Fore, Style
init(autoreset=True)

def main():
    initializeTable()
    
    while True:
        print(Fore.CYAN + Style.BRIGHT + "-----------------")
        print(Fore.CYAN + Style.BRIGHT + "Financial Tracker Menu")
        print(Fore.CYAN + Style.BRIGHT + "-----------------")
        print(Fore.GREEN + "1. Add new entry")
        print(Fore.GREEN + "2. Delete an entry")
        print(Fore.GREEN + "3. Display current finances")
        print(Fore.GREEN + "4. Graph current finances")
        print(Fore.RED + "5. Exit")
        print(Fore.CYAN + "-----------------")
        
        choice = input(Fore.CYAN + "Choose an option (1-5): ")
        
        if choice == '1':
            userInputs()
            print(Fore.GREEN + "ENTRY ADDED")
        elif choice == '2':
            print(Fore.CYAN + Style.BRIGHT + "-----------------")
            print(Fore.CYAN + Style.BRIGHT + "Delete An Entry")
            print(Fore.CYAN + Style.BRIGHT + "-----------------")
            letter = str(input((Fore.RED + "Are you sure you want to delete an entry? (Y/N): ")))
            if letter == "Y":
                while True:
                    date = input((Fore.RED + "Enter the date you want to delete or EXIT to quit: "))
                    if date == "EXIT":
                        break
                    elif re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$', date):
                        if deleteFromDatabase(date):
                            print(Fore.RED + "ENTRY [" + date + "] DELETED")
                        else:
                            print(Fore.RED + Style.BRIGHT + "DATE DOES NOT EXIST. RETURNING TO MAIN MENU")
                        break
                    else:
                        print(Fore.RED + Style.BRIGHT + "Invalid date format.")
        elif choice == '3':
            print(Fore.CYAN + Style.BRIGHT + "-----------------")
            print(Fore.CYAN + Style.BRIGHT + "Current Finances")
            print(Fore.CYAN + Style.BRIGHT + "-----------------")
            displayDatabase()
        elif choice == '4':
            print(Fore.CYAN + Style.BRIGHT + "-----------------")
            print(Fore.CYAN + Style.BRIGHT + "Graphing Finances")
            print(Fore.CYAN + Style.BRIGHT + "-----------------")
            graphFinances()
        elif choice == '5':
            print(Fore.GREEN + "Exiting the Financial Tracker...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option (1-5).")
            
        
def initializeTable():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS tracker (
                date TEXT,
                chase REAL,
                amex REAL,
                citi REAL,
                roth REAL,
                total REAL
                    )''')
    
    conn.commit()
    conn.close()

def userInputs():
    print(Fore.CYAN + Style.BRIGHT + "-----------------")
    print(Fore.CYAN + Style.BRIGHT + "Add New Entry")
    print(Fore.CYAN + Style.BRIGHT + "-----------------")
    while True:
        date = input(Fore.CYAN + "Enter the date (MM/DD/YYYY): ")
        if re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$', date):
            break
        else:
            print("Invalid date format.")

    chase = float(input(Fore.CYAN + "Amount in CHASE: "))
    amex = float(input(Fore.CYAN + "Amount in AMEX: "))
    citi = float(input(Fore.CYAN + "Amount in CITI: "))
    roth = float(input(Fore.CYAN + "Amount in Roth IRA: "))

    addToDatabase(date, chase, amex, citi, roth)

def addToDatabase(date, chase, amex, citi, roth):
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()

    total = chase + amex + citi + roth
    
    c.execute('''INSERT INTO tracker (date, chase, amex, citi, roth, total)
                VALUES (?, ?, ?, ?, ?, ?)''', (date, chase, amex, citi, roth, total))
    conn.commit()
    conn.close()

def recentPieChart():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()

    pieChart= str(input(Fore.CYAN + "View the pie chart distribution? (Y/N): "))
    if pieChart == "Y":
        c.execute('''SELECT * FROM tracker ORDER BY date DESC LIMIT 1''')
        most_recent = c.fetchone()
        
        date, chase, amex, citi, roth, total = most_recent
        labels = ['Chase', 'AMEX', 'Citi', 'Roth IRA']
        sizes = [chase, amex, citi, roth]
        colors = ['steelblue', 'darkslateblue', 'darkgoldenrod', 'forestgreen']
            
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                    shadow=True, startangle=140)

        plt.title(f"Distribution for: {date}")
        plt.show()

        conn.close()

def displayDatabase():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('''SELECT *
                FROM tracker''')
    rows = c.fetchall()
    print("DATE        | CHASE $  | AMEX $   | CITI $   | ROTH $   | TOTAL")
    print("------------|----------|----------|----------|----------|----------")
    
    for row in rows:
        date, chase, amex, citi, roth, total = row
        print(f"{date:<11} | {chase:>8.2f} | {amex:>8.2f} | {citi:>8.2f} | {roth:>8.2f} | {total:>8.2f}")

    conn.close()

    recentPieChart()

def clearDatabase():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('''DELETE FROM tracker''')
    conn.commit()
    conn.close()

def unique_digits(input_string):
    digits_set = set(input_string)
    return len(digits_set) == len(input_string)


def graphFinances():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('''SELECT *
                FROM tracker''')
    rows = c.fetchall()
    xAXIS, yAXISTotal, yAXISChase, yAXISAmex, yAXISCiti, yAXISRoth = [], [], [], [], [], []
    for row in rows:
        date, chase, amex, citi, roth, total = row
        xAXIS.append(date)
        yAXISTotal.append(total)
        yAXISChase.append(chase)
        yAXISAmex.append(amex)
        yAXISCiti.append(citi)
        yAXISRoth.append(roth)
    
    print(Fore.GREEN + "1: Total")
    print(Fore.GREEN + "2: Chase")
    print(Fore.GREEN + "3: AMEX")
    print(Fore.GREEN + "4: Citi")
    print(Fore.GREEN + "5: ROTH IRA")
    print(Fore.CYAN + "-----------------")
    amount = str(input(Fore.CYAN + "Enter your choices consecutively (ex. 123): "))
    if len(amount) < 5 and unique_digits(amount):
        for i in range(len(amount)):
            if amount[i] == '1':
                plt.plot(xAXIS, yAXISTotal, label = "Total")
            elif amount[i] == '2':
                plt.plot(xAXIS, yAXISChase, label = "Chase")
            elif amount[i] == '3':
                plt.plot(xAXIS, yAXISAmex, label = "Amex")
            elif amount[i] == '4':
                plt.plot(xAXIS, yAXISCiti, label = "Citi")
            elif amount[i] == '5':
                plt.plot(xAXIS, yAXISRoth, label = "Roth IRA")
            else:
                print(Fore.RED + Style.BRIGHT + "Invalid Number Detected, Terminating.")
                break;
        plt.xlabel('TIME')
        plt.ylabel('Money')
        plt.title('Money Over Time')
        plt.legend()
        plt.show()
    else:
        print(Fore.RED + Style.BRIGHT + "Input Invalid.\nTry unique numbers or not exceeding 5 entries.")
    
def deleteFromDatabase(date_):
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    # check if valid
    c.execute('''SELECT * FROM tracker WHERE date = ?''', (date_,))
    record = c.fetchone()
    
    if record:
        # Date exists, proceed to delete
        c.execute('''DELETE FROM tracker WHERE date = ?''', (date_,))
        conn.commit()
        return True
    else:
        # Date does not exist
        return False

if __name__ == '__main__':
    main()