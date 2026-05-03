# app/db/supabase_client.py
from supabase import create_client, Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            cls._instance = create_client(settings.supabase_url, settings.supabase_key)
            logger.info("✅ Supabase connected")
        return cls._instance
    
    @classmethod
    async def get_customer_by_mobile(cls, mobile: str):
        client = cls.get_client()
        result = client.table("customers").select("*").eq("mobile_number", mobile).execute()
        return result.data[0] if result.data else None
    
    @classmethod
    async def get_customer_by_pppoe(cls, pppoe_name: str):
        client = cls.get_client()
        result = client.table("customers").select("*").eq("pppoe_name", pppoe_name).execute()
        return result.data[0] if result.data else None
    
    @classmethod
    async def get_customer_by_telegram_id(cls, telegram_id: str):
        client = cls.get_client()
        result = client.table("customers").select("*").eq("telegram_id", telegram_id).execute()
        return result.data[0] if result.data else None
    
    @classmethod
    async def create_ticket(cls, ticket_data: dict):
        client = cls.get_client()
        result = client.table("tickets").insert(ticket_data).execute()
        return result.data[0] if result.data else None
    
    @classmethod
    async def get_tenant(cls, tenant_id: str):
        client = cls.get_client()
        result = client.table("tenants").select("*").eq("id", tenant_id).execute()
        return result.data[0] if result.data else None
    
    @classmethod
    async def update_customer_status(cls, customer_id: str, status: str, signal_dbm: float = None):
        client = cls.get_client()
        update_data = {"status": status}
        if signal_dbm:
            update_data["last_signal_dbm"] = signal_dbm
        result = client.table("customers").update(update_data).eq("id", customer_id).execute()
        return result.data[0] if result.data else None