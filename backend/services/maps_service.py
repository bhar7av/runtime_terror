def get_nearby_doctors_link(doctor_type: str) -> str:
    """
    Returns a Google Maps URL searching for the recommended doctor near the user.
    """
    if not doctor_type:
        return ""
    
    # Strip basic safety phrases if needed
    query = f"{doctor_type} near me".replace(" ", "+")
    return f"https://www.google.com/maps/search/{query}"
