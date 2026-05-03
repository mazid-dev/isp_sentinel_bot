# app/services/orchestrator.py
from app.services.ai_service import AIService
from app.services.network_service import NetworkService
from app.services.ticket_service import TicketService
from app.db.supabase_client import SupabaseClient
import logging
import re

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.ai = AIService()
        self.network = NetworkService()
        self.ticket = TicketService()
        self.supabase = SupabaseClient()
    
    async def process_customer_query(self, user_input: str, sender_id: str) -> str:
        logger.info(f"📨 Query: {user_input[:50]}")
        
        # Identify customer
        customer = await self._identify_customer(user_input, sender_id)
        if not customer:
            return self._get_not_found_response()
        
        # Check network status
        network_status = await self.network.check_customer_status(customer)
        
        # AI diagnosis
        diagnosis = await self.ai.diagnose_network_issue(customer, network_status)
        
        # Create ticket if needed
        response = diagnosis.get('diagnosis', '')
        if diagnosis.get('auto_ticket'):
            ticket = await self.ticket.create_auto_ticket(customer['id'], diagnosis, network_status)
            response += f"\n\n🎫 টিকেট: {ticket.get('id', '')[:8]}"
            response += f"\n💡 {diagnosis.get('suggested_action', '')}"
        
        return response
    
    async def _identify_customer(self, user_input: str, sender_id: str) -> dict:
        # Mobile number
        mobile_match = re.search(r'01[3-9]\d{8}', user_input)
        if mobile_match:
            customer = await self.supabase.get_customer_by_mobile(mobile_match.group())
            if customer:
                return customer
        
        # PPPoE
        if '@' in user_input:
            customer = await self.supabase.get_customer_by_pppoe(user_input.strip())
            if customer:
                return customer
        
        # Telegram ID
        customer = await self.supabase.get_customer_by_telegram_id(sender_id)
        return customer
    
    def _get_not_found_response(self) -> str:
        return """❌ আপনার তথ্য পাওয়া যায়নি।

দয়া করে আপনার রেজিস্টার্ড মোবাইল নাম্বার লিখুন:
017xxxxxxxx

অথবা PPPoE ইউজারনেম লিখুন"""