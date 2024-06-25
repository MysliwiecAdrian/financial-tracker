# Financial app

import sqlite3
import re
import matplotlib.pyplot as plt
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
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            userInputs()
            print(Fore.GREEN + "ENTRY ADDED")
        elif choice == '2':
            letter = str(input((Fore.RED + "Are you sure you want to delete an entry? (Y/N): ")))
            if letter == "Y":
                while True:
                    date = input((Fore.RED + "Enter the date you want to delete or EXIT to quit: "))
                    if date == "EXIT":
                        break
                    elif re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$', date):
                        deleteFromDatabase(date)
                        print(Fore.RED + "ENTRY [" + date + "] DELETED")
                        break
                    else:
                        print("Invalid date format.")
        elif choice == '3':
            displayDatabase()
        elif choice == '4':
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
    print("Enter today's date with your current finances\n")
    while True:
        date = input("Enter the date (MM/DD/YYYY): ")
        if re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$', date):
            break
        else:
            print("Invalid date format.")

    chase = float(input("Amount in CHASE: "))
    amex = float(input("Amount in AMEX: "))
    citi = float(input("Amount in CITI: "))
    roth = float(input("Amount in Roth IRA: "))

    addToDatabase(date, chase, amex, citi, roth)

def addToDatabase(date, chase, amex, citi, roth):
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()

    total = chase + amex + citi + roth
    
    c.execute('''INSERT INTO tracker (date, chase, amex, citi, roth, total)
                VALUES (?, ?, ?, ?, ?, ?)''', (date, chase, amex, citi, roth, total))
    conn.commit()
    conn.close()

def displayDatabase():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('''SELECT *
                FROM tracker''')
    rows = c.fetchall()
    print("\nDATE        | CHASE $  | AMEX $   | CITI $   | ROTH $   | TOTAL")
    print("------------|----------|----------|----------|----------|----------")
    
    for row in rows:
        date, chase, amex, citi, roth, total = row
        print(f"{date:<11} | {chase:>8.2f} | {amex:>8.2f} | {citi:>8.2f} | {roth:>8.2f} | {total:>8.2f}")


    conn.close()

def clearDatabase():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('''DELETE FROM tracker''')
    conn.commit()
    conn.close()

def graphFinances():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute('''SELECT *
                FROM tracker''')
    rows = c.fetchall()
    xAXIS, yAXIS = [], []
    for row in rows:
        date, chase, amex, citi, roth, total = row
        xAXIS.append(date)
        yAXIS.append(total)
    
    plt.plot(xAXIS, yAXIS)
    plt.xlabel('TIME')
    plt.ylabel('TOTAL')
    plt.title('Total $ Over Time')

    plt.show()

def deleteFromDatabase(date_):
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    # check if valid
    c.execute('''DELETE FROM tracker
                WHERE date = ?''', (date_,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()