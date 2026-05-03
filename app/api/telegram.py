# app/api/telegram.py
from fastapi import APIRouter, Request
from telegram import Bot
from app.services.orchestrator import Orchestrator
from app.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

bot = Bot(token=settings.telegram_bot_token)
orchestrator = Orchestrator()

@router.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        
        if 'message' in data and 'text' in data['message']:
            user_msg = data['message']['text']
            chat_id = data['message']['chat']['id']
            sender_id = str(data['message']['from']['id'])
            
            response = await orchestrator.process_customer_query(user_msg, sender_id)
            await bot.send_message(chat_id=chat_id, text=response)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error"}