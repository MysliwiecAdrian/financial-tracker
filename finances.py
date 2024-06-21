# Financial app

import sqlite3
import re


def main():
    initializeTable()
    userInputs()

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
        date = input("Enter the date (MM/YYYY): ")
        if re.match(r'^(0[1-9]|1[0-2])\/\d{4}', date):
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
                VALUES (?, ?, ?, ?, ?)''', (date, chase, amex, citi, roth, total))
    conn.commit()
    conn.close()

def displayTable():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()


if __name__ == '__main__':
    main()