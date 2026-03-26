"""
Demo Mode — Voice Agent Simulator
Runs a pre-scripted conversation showing the agent handling
a realistic scenario, including a graceful escalation.
Designed for README demos and screen recordings.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import get_agent_response, stream_print, AGENT_PERSONA
from tools.escalation import check_escalation, escalation_message

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GREEN  = "\033[92m"
DIM    = "\033[2m"

DEMO_SCRIPT = [
    "Hi, I'd like to book an appointment.",
    "My name is Sarah. I need a cleaning, preferably next Thursday.",
    "Morning is fine, around 9 or 10 AM.",
    "Do you accept Delta Dental insurance?",
    "Actually, can I speak to a real person? I have a complicated situation.",
]

PAUSE_BETWEEN_TURNS = 1.5   # seconds


def run_demo() -> None:
    agent_name = AGENT_PERSONA["name"]

    print(f"\n{BOLD}{GREEN}{'─' * 55}{RESET}")
    print(f"{BOLD}{GREEN}  🦷  DEMO MODE — BrightSmile Voice Agent{RESET}")
    print(f"{BOLD}{GREEN}{'─' * 55}{RESET}")
    print(f"{DIM}  This is a pre-scripted demo conversation.{RESET}")
    print(f"{DIM}  Watching it? Try 'python agent.py' for live mode.{RESET}")
    print(f"{BOLD}{GREEN}{'─' * 55}{RESET}\n")

    history = []

    # Greeting
    greeting = (
        f"Thank you for calling BrightSmile Dental Clinic, "
        f"my name is {agent_name} and I'm here to help. "
        f"How can I assist you today?"
    )
    print(f"{YELLOW}{BOLD}  {agent_name}:{RESET} ", end="")
    stream_print(greeting)
    time.sleep(PAUSE_BETWEEN_TURNS)

    for user_input in DEMO_SCRIPT:
        print(f"{BOLD}  You:{RESET} {user_input}\n")
        time.sleep(0.6)

        history.append({"role": "user", "content": user_input})

        # Check escalation
        escalation = check_escalation(user_input, history)
        if escalation["escalate"]:
            print(f"{DIM}  [ESCALATION TRIGGERED] {escalation['reason']}{RESET}")
            response = escalation_message(agent_name)
            print(f"{RED}{BOLD}  {agent_name} [escalating]:{RESET} ", end="")
            stream_print(response, color=RED)
            print(f"{DIM}  — Demo complete: session transferred to human staff —{RESET}\n")
            return

        # Agent response
        print(f"{DIM}  [thinking...]{RESET}", end="\r")
        response = get_agent_response(history)
        print(" " * 20, end="\r")

        history.append({"role": "assistant", "content": response})

        print(f"{YELLOW}{BOLD}  {agent_name}:{RESET} ", end="")
        stream_print(response)
        time.sleep(PAUSE_BETWEEN_TURNS)

    print(f"{DIM}  — Demo complete —{RESET}\n")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print(f"{RED}Error: OPENAI_API_KEY environment variable not set.{RESET}")
        sys.exit(1)
    run_demo()
