"""
Escalation & Fallback Logic — Voice Agent Simulator
Detects when the agent should escalate to a human or trigger a fallback.
"""

# Phrases that immediately trigger human escalation
ESCALATION_TRIGGERS = [
    "speak to someone",
    "talk to a human",
    "real person",
    "representative",
    "agent",
    "manager",
    "this is ridiculous",
    "unacceptable",
    "i give up",
    "forget it",
    "this is useless",
]

# Sentiment signals suggesting growing frustration
FRUSTRATION_SIGNALS = [
    "still not",
    "already told you",
    "you don't understand",
    "that's not what i said",
    "not helpful",
    "wrong",
    "stop",
    "ugh",
    "seriously",
    "come on",
]

# Max times the same intent can repeat before forced escalation
REPETITION_THRESHOLD = 3


def check_escalation(user_input: str, conversation_history: list) -> dict:
    """
    Analyse user input and conversation history.
    Returns a dict with:
        - escalate (bool): whether to escalate
        - reason (str): reason for escalation, or empty string
    """
    text = user_input.lower()

    # Hard trigger — immediate escalation
    for trigger in ESCALATION_TRIGGERS:
        if trigger in text:
            return {
                "escalate": True,
                "reason": f"Hard trigger detected: '{trigger}'",
            }

    # Frustration signals
    frustration_count = sum(1 for signal in FRUSTRATION_SIGNALS if signal in text)
    if frustration_count >= 2:
        return {
            "escalate": True,
            "reason": f"High frustration signal ({frustration_count} markers detected)",
        }

    # Repetition check — count how many user turns contain similar short phrases
    user_turns = [
        m["content"].lower()
        for m in conversation_history
        if m["role"] == "user"
    ]
    if len(user_turns) >= REPETITION_THRESHOLD:
        # Check if last N user turns are suspiciously similar in length and content
        recent = user_turns[-REPETITION_THRESHOLD:]
        if all(abs(len(t) - len(recent[0])) < 15 for t in recent):
            return {
                "escalate": True,
                "reason": "Repetition threshold reached — user may be stuck in a loop",
            }

    return {"escalate": False, "reason": ""}


def escalation_message(agent_name: str) -> str:
    """Return a natural escalation message spoken by the agent."""
    return (
        f"I understand, and I'm sorry I haven't been able to fully help. "
        f"Let me connect you with a member of our team who can assist you directly — "
        f"please hold for just a moment."
    )


def fallback_message(agent_name: str) -> str:
    """Return a natural fallback message for unclear input."""
    return (
        f"I'm sorry, I didn't quite catch that. "
        f"I can help you book or manage appointments, or answer questions about our clinic — "
        f"which would you like?"
    )
