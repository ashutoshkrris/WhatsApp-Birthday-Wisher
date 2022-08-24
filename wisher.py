def send_birthday_wish(client, recipient_number, recipient_name):

    birthday_wish = f"Hey {recipient_name}, Happy Birthday to you from Ashutosh!"

    try:
        client.messages.create(
            body=birthday_wish,
            from_="whatsapp:+14155238886",
            to=f"whatsapp:{recipient_number}"
        )

        print("Message sent to", recipient_name,
              "on WhatsApp number", recipient_number)
        return True

    except Exception:
        print("Something went wrong. Birthday message not sent.")
        return False
