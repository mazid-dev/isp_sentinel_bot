# app/services/network_service.py
from app.integrations.mikrotik import MikroTikClient
from app.integrations.olt import OLTMonitor
from app.db.supabase_client import SupabaseClient
import logging

logger = logging.getLogger(__name__)

class NetworkService:
    def __init__(self):
        self.supabase = SupabaseClient()
        self.mikrotik_clients = {}
    
    async def get_mikrotik_client(self, tenant_id: str):
        if tenant_id not in self.mikrotik_clients:
            tenant = await self.supabase.get_tenant(tenant_id)
            if tenant and tenant.get('mikrotik_host'):
                self.mikrotik_clients[tenant_id] = MikroTikClient(
                    host=tenant['mikrotik_host'],
                    username=tenant['mikrotik_user'],
                    password=tenant['mikrotik_password']
                )
        return self.mikrotik_clients.get(tenant_id)
    
    async def check_customer_status(self, customer: dict) -> dict:
        tenant_id = customer['tenant_id']
        mikrotik = await self.get_mikrotik_client(tenant_id)
        
        result = {"pppoe_online": False, "signal_dbm": None, "mass_outage_count": 0}
        
        if mikrotik:
            pppoe_status = await mikrotik.get_pppoe_status(customer.get('pppoe_name', ''))
            result["pppoe_online"] = pppoe_status.get('online', False)
        
        if customer.get('mac_address'):
            olt = OLTMonitor(mikrotik, customer.get('olt_ip', '192.168.1.1'))
            result["signal_dbm"] = await olt.get_onu_signal_by_mac(customer['mac_address'])
        
        return result