This project is a Telegram bot designed to manage and report various sales and postal data. The bot uses the Aiogram framework for Telegram Bot API, and SQLite for database management. Below is an explanation of the bot's functionality and how to set it up.

Table of Contents

Features
Requirements
Installation
Usage
Database Schema
Contributing

Features

Start Command: Initializes the bot and provides a welcome message.
Best Employees of the Month: Displays the top employees based on sales and EMS.
Monthly Plan Submission: Collects and stores monthly sales and postal plans.
Daily Report Submission: Allows users to submit their daily reports.
View Reports: Provides a summary report of sales and postal data for the day and month.
Email Report: Sends the report via email to a specified user.
Data Visualization: Generates and sends visual representations of the data.
Admin Panel: Restricted access commands for administrative tasks.
Clear Data: Deletes all records from the database.

Requirements

Python 3.7+
Aiogram
SQLite
Pandas
Seaborn
Matplotlib
BeautifulSoup
Requests
Emoji



Installation

git clone https://github.com/ufukkirmizigedik/telegram-bot.git
cd telegram-bot

Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Dependencies:
pip install -r requirements.txt

Set Up Environment Variables:
Create a .env file in the root directory and add your bot token:
API_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

Run the Bot:
python bot.py


Usage
/start: Initiates the bot and displays the welcome message.

/Лучшее_сотрудники_месяца: Displays the best employees of the month based on sales and EMS.

/План_месяц: Starts the process of submitting the monthly plan.

/Отправить_отчет: Begins the daily report submission process.

/Отчет_дня: Shows the summary of the day's sales and postal data.

/Отчет_месяца: Shows the summary of the month's sales and postal data.

/Email: Sends the monthly report via email (Admin only).

/Дата_визуализация: Generates and sends data visualizations.

/План: Displays the current month's plan.

/Delete_all: Clears all records from the database (Admin only).

/Admin: Accesses the admin panel (Admin only).

/Отчет_ваш: Displays the user's personal monthly report.

Database Schema
The bot uses SQLite for data storage with the following schema:

fakt table:

user_id: INTEGER
name: TEXT
ems: INTEGER
pismo: INTEGER
posilka: INTEGER
sale: INTEGER
data: TEXT
plan table:

plan_sales: INTEGER
plan_ems: INTEGER
plan_pismo: INTEGER
plan_posilka: INTEGER
data: TEXT
Contributing
Fork the repository.
Create a new branch.
Make your changes.
Submit a pull request.
