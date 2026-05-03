# app/integrations/mikrotik.py
import librouteros
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

class MikroTikClient:
    def __init__(self, host: str, username: str, password: str, port: int = 8728):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self._connection = None
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def connect(self):
        try:
            self._connection = librouteros.connect(
                host=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                timeout=10
            )
            logger.info(f"✅ Connected to MikroTik: {self.host}")
            return self._connection
        except Exception as e:
            logger.error(f"❌ MikroTik connection failed: {e}")
            raise Exception(f"Cannot connect: {e}")
    
    async def get_pppoe_status(self, pppoe_name: str) -> dict:
        if not self._connection:
            await self.connect()
        
        try:
            secrets = list(self._connection.path('ppp', 'secret'))
            for secret in secrets:
                if secret.get('name') == pppoe_name:
                    return {
                        "online": not secret.get('disabled', True),
                        "caller_id": secret.get('caller-id', 'unknown'),
                        "uptime": secret.get('uptime', '0s')
                    }
            return {"online": False, "error": "user_not_found"}
        except Exception as e:
            logger.error(f"PPPoE check failed: {e}")
            return {"online": False, "error": str(e)}