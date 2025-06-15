class FollowUpAgent:
    """
    Agent to suggest follow-up actions (e.g., directions or booking) for the top business result.
    """
    def suggest(self, top_results):
        """
        Suggest a follow-up action based on the top result.

        Args:
            top_results (list): List of top business dicts.

        Returns:
            str or None: Follow-up suggestion string or None if no results.
        """
        if not top_results:
            return None
        # Always offer directions or booking for the top result
        name = top_results[0]["name"]
        return f"Would you like directions to {name}? Or want me to book a table?"
