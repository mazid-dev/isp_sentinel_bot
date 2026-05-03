# app/services/ai_service.py
import google.generativeai as genai
from app.config import settings
import json
import logging
import re

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def diagnose_network_issue(self, customer_info: dict, network_status: dict) -> dict:
        prompt = f"""তুমি ISP নেটওয়ার্ক ইঞ্জিনিয়ার AI।

গ্রাহক: {customer_info.get('customer_code', 'Unknown')}
PPPoE: {'অনলাইন' if network_status.get('pppoe_online') else 'অফলাইন'}
সিগন্যাল: {network_status.get('signal_dbm', 'N/A')} dBm
এলাকায় অফলাইন: {network_status.get('mass_outage_count', 0)} জন

JSON আউটপুট দাও:
{{"diagnosis": "বাংলায় সমস্যা", "severity": "low/medium/critical", "auto_ticket": true/false, "suggested_action": "বাংলায় করণীয়"}}"""

        try:
            response = self.model.generate_content(prompt)
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return self._fallback_diagnosis(network_status)
        except:
            return self._fallback_diagnosis(network_status)
    
    def _fallback_diagnosis(self, network_status: dict) -> dict:
        signal = network_status.get('signal_dbm', 0)
        pppoe_online = network_status.get('pppoe_online', False)
        
        if network_status.get('mass_outage_count', 0) > 3:
            return {"diagnosis": "ফাইবার কাট হয়েছে", "severity": "critical", "auto_ticket": True, "suggested_action": "টেকনিশিয়ান কাজ করছে"}
        elif signal < -27:
            return {"diagnosis": f"সিগন্যাল দুর্বল ({signal} dBm)", "severity": "medium", "auto_ticket": True, "suggested_action": "প্যাচ কর্ড চেক করুন"}
        elif not pppoe_online:
            return {"diagnosis": "PPPoE অফলাইন", "severity": "medium", "auto_ticket": True, "suggested_action": "বিলিং চেক করুন"}
        else:
            return {"diagnosis": "নেটওয়ার্ক ঠিক আছে", "severity": "low", "auto_ticket": False, "suggested_action": "রাউটার রিস্টার্ট দিন"}