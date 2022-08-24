from datetime import datetime
import os

import pandas as pd
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from wisher import send_birthday_wish

account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
client = Client(account_sid, auth_token)

app = Flask(__name__)


def create_birthdays_dataframe():
    try:
        birthdays_df = pd.read_csv("data.csv")
        birthdays_df["Bday"] = pd.to_datetime(
            birthdays_df["Bday"], format="%d-%m-%Y")
        return birthdays_df

    except Exception as e:
        print(e)
        print("Something went wrong. Birthdays dataframe not created.")
        return False


def check_for_birthdays():
    try:
        birthdays_df = create_birthdays_dataframe()
        birthdays_df["day"] = birthdays_df["Bday"].dt.day
        birthdays_df["month"] = birthdays_df["Bday"].dt.month
        today = datetime.now()
        for i in range(birthdays_df.shape[0]):
            birthday_day = birthdays_df.loc[i, "day"]
            birthday_month = birthdays_df.loc[i, "month"]
            if today.day == birthday_day and today.month == birthday_month:
                send_birthday_wish(
                    client,
                    birthdays_df.loc[i, "Number"],
                    birthdays_df.loc[i, "Name"]
                )
        return True

    except Exception:
        print("Something went wrong. Birthday check not successful.")
        return False


scheduler = BackgroundScheduler()
job = scheduler.add_job(check_for_birthdays, 'cron',
                        day_of_week='mon-sun', hour=12, minute=9)
scheduler.start()

if __name__ == "__main__":
    app.run()
