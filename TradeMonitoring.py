import asyncio
import json
import websockets

async def subscribe_to_stock():
    async with websockets.connect('ws://enter-your-stock-url') as websocket:
        subscribe_message = json.dumps({'type': 'subscribe', 'symbol': 'your-stock-symbol'})
        await websocket.send(subscribe_message)
        current_price = None
        async for message in websocket:
            trade_data = json.loads(message)
            if current_price and trade_data["price"] < current_price:
                current_price = trade_data["price"]
                send_notification("Stock price is falling")
            else:
                current_price = trade_data["price"]
                
def send_notification(message):
    # this section is pending 

asyncio.get_event_loop().run_until_complete(subscribe_to_stock())