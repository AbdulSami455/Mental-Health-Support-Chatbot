def chat_bubble(sender, message):
    """Return HTML for a chat bubble."""
    if sender == "You":
        return f"""
        <div style='text-align: right; margin: 10px 0;'>
            <div style='display: inline-block; background-color: #ADD8E6; color: black; padding: 10px; border-radius: 10px; max-width: 70%;'>
                <strong>You:</strong><br>{message}
            </div>
        </div>
        """
    else:
        return f"""
        <div style='text-align: left; margin: 10px 0;'>
            <div style='display: inline-block; background-color: #ECECEC; color: black; padding: 10px; border-radius: 10px; max-width: 70%;'>
                <strong>Assistant:</strong><br>{message}
            </div>
        </div>
        """
