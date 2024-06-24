# Financial app

import sqlite3
import re
import pandas as pd
import matplotlib.pyplot as plt


def main():
    initializeTable()
    # userInputs()
    # clearDatabase()
    displayDatabase()
    # graphFinances()

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
    plt.title('Graph')

    plt.show()

if __name__ == '__main__':
    main()