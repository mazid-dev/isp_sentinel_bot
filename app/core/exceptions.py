# app/core/exceptions.py

class ISPSentinelError(Exception):
    """Base exception"""
    pass

class MikroTikConnectionError(ISPSentinelError):
    """MikroTik connection failed"""
    pass

class GeminiapiError(ISPSentinelError):
    """Gemini API failed"""
    pass

class CustomerNotFoundError(ISPSentinelError):
    """Customer not found"""
    pass