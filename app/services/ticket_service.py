# app/services/ticket_service.py
from app.db.supabase_client import SupabaseClient
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

class TicketService:
    def __init__(self):
        self.supabase = SupabaseClient()
    
    async def create_auto_ticket(self, customer_id: str, diagnosis: dict, network_status: dict) -> dict:
        ticket_data = {
            "id": str(uuid.uuid4()),
            "customer_id": customer_id,
            "issue_type": self._get_issue_type(diagnosis, network_status),
            "severity": diagnosis.get('severity', 'medium'),
            "diagnosis": diagnosis.get('diagnosis', 'Unknown'),
            "status": "open",
            "created_at": datetime.utcnow().isoformat()
        }
        result = await self.supabase.create_ticket(ticket_data)
        logger.info(f"🎫 Ticket created: {result.get('id', '')[:8]}")
        return result or ticket_data
    
    def _get_issue_type(self, diagnosis: dict, network_status: dict) -> str:
        if network_status.get('mass_outage_count', 0) > 3:
            return "fiber_cut"
        elif network_status.get('signal_dbm', 0) < -27:
            return "low_signal"
        elif not network_status.get('pppoe_online'):
            return "offline"
        return "other"