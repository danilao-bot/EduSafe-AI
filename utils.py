"""
Utility functions for EduSafe AI system
"""

# Currency conversion constants
USD_TO_NAIRA = 1300

def convert_usd_to_naira(usd_amount):
    """
    Convert USD amount to Nigerian Naira.
    
    Args:
        usd_amount (float): Amount in USD
        
    Returns:
        float: Amount converted to Naira
    """
    if usd_amount is None:
        return None
    return usd_amount * USD_TO_NAIRA


def convert_naira_to_usd(naira_amount):
    """
    Convert Naira amount back to USD.
    
    Args:
        naira_amount (float): Amount in Naira
        
    Returns:
        float: Amount converted to USD
    """
    if naira_amount is None:
        return None
    return naira_amount / USD_TO_NAIRA


def format_naira(amount):
    """
    Format amount as Nigerian Naira currency string.
    
    Args:
        amount (float): Amount in Naira
        
    Returns:
        str: Formatted currency string (e.g., "₦1,300,000")
    """
    if amount is None:
        return "N/A"
    return f"₦{int(amount):,}"


def employment_status_display(status_code):
    """
    Convert employment status code to display text.
    
    Args:
        status_code (int): 0 or 1 (model representation)
        
    Returns:
        str: "No" or "Yes" for display
    """
    if status_code is None:
        return "Unknown"
    return "Yes" if status_code == 1 else "No"
