from fastapi import FastAPI, Request
import telegram
import os
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Telegram bot setup
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN else None

@app.get("/")
async def home():
    return {"message": "Trading Bot is Live! 🚀", "status": "success"}

@app.post("/webhook")
async def webhook_listener(request: Request):
    try:
        data = await request.json()
        logger.info(f"Received webhook data: {data}")
        
        # Strategy 1 Alert Processing
        if data.get('type') == 'strategy1':
            message = f"""
🚀 **Strategy 1 Signal Received!**
▸ Symbol: {data.get('symbol', 'N/A')}
▸ Action: {data.get('action', 'N/A')}
▸ Price: {data.get('price', 'N/A')}
▸ Timeframe: {data.get('tf', 'N/A')}
▸ Strategy: Zero Lag + Smart Money Toolkit
            """
            
            if bot and TELEGRAM_CHAT_ID:
                await bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=message,
                    parse_mode='Markdown'
                )
            
            return {"status": "success", "message": "Strategy 1 alert processed"}
        
        return {"status": "error", "message": "Unknown alert type"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
