# app/integrations/olt.py
from app.integrations.mikrotik import MikroTikClient
import logging
import hashlib
import random

logger = logging.getLogger(__name__)

class OLTMonitor:
    def __init__(self, mikrotik_client: MikroTikClient, olt_ip: str, community: str = 'public'):
        self.mikrotik = mikrotik_client
        self.olt_ip = olt_ip
        self.community = community
    
    async def get_onu_signal_by_mac(self, mac_address: str) -> float:
        """
        ⚠️ এখানে আপনার OLT এর SNMP OID দিতে হবে (নিচে দেখুন)
        """
        try:
            logger.info(f"📡 Fetching signal for MAC: {mac_address}")
            
            # ============================================
            # 🔧 আপনার OLT মডেল অনুযায়ী নিচের OID পরিবর্তন করুন
            # ============================================
            
            # Huawei OLT এর জন্য:
            oid = "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4"
            
            # ZTE OLT এর জন্য (কমেন্ট খুলুন):
            # oid = "1.3.6.1.4.1.3902.3.100.1.1.2.1.1.4"
            
            # Nokia OLT এর জন্য (কমেন্ট খুলুন):
            # oid = "1.3.6.1.4.1.637.61.1.23.1.1.4"
            
            # ============================================
            # Mock data (টেস্টিং এর জন্য - OLT না থাকলেও কাজ করবে)
            # ============================================
            hash_val = int(hashlib.md5(mac_address.encode()).hexdigest()[:8], 16)
            signal = -15 - (hash_val % 25)
            return float(signal)
            
        except Exception as e:
            logger.error(f"OLT signal failed: {e}")
            return -99.0