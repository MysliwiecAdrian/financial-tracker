# Financial Tracker

> [!IMPORTANT]
> This project has been created for personal use. It only stores my current financial amount and the accounts associated with them. It could be modified to fit personal needs but that would require adjusting various implementation within the code. As of 7/18/2024, use for multiple accounts is currently not supported.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Libraries](#libraries)

## Introduction
The Financial Tracker is a simple Python application that helps users track their finances across multiple accounts. It allows users to add, delete, view, and graph their financial data.

## Features
- Add new financial entries with the date and amounts in different accounts.
- Delete existing entries.
- Display all financial entries in a tabular format.
- Graph financial data over time.
- Visualize the most recent financial distribution with a pie chart.

## Usage
To start the program, run the following command
```
python finances.py
```
### Menu Options
1. Add new entry: Prompts the user to enter the date and amounts for each account, then saves this information to the database.
2. Delete an entry: Prompts the user to enter the date of the entry they wish to delete.
3. Display current finances: Displays all financial entries in a tabular format and shows a pie chart of the most recent entry.
4. Graph current finances: Allows the user to graph financial data over time for selected accounts.
5. Exit: Exits the application.

## Libraries
- SQLite
- RE
- Matplotlib
- Pandas
- Colorama
