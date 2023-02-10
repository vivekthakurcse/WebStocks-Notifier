import asyncio
import json
import websockets
import smtplib

async def subscribe_to_stock():
    async with websockets.connect('ws://enter-your-stock-url') as websocket:
        subscribe_message = json.dumps({'type': 'subscribe', 'symbol': 'your-stock-symbol'})
        await websocket.send(subscribe_message)
        current_price = None
        async for message in websocket:
            try:
                trade_data = json.loads(message)
                if current_price and trade_data["price"] < current_price:
                    current_price = trade_data["price"]
                    send_notification("Stock price is falling")
                else:
                    current_price = trade_data["price"]
            except Exception as e:
                print(f"Error processing message: {e}")

def send_notification(message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("your-email-address@gmail.com", "your-email-password")
        subject = "Stock Price Alert"
        body = message
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("your-email-address@gmail.com", "to-email-address@gmail.com", msg)
        print(f"Successfully sent email to {to_email}")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(subscribe_to_stock())
