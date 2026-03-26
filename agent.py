"""
Voice Agent Simulator — Core Conversation Loop
Simulates a Retell AI / ElevenLabs-style voice agent in the terminal.
Uses OpenAI GPT-4o as the language model backend.
"""

import os
import time
import sys
from openai import OpenAI
from prompts.system_prompt import build_system_prompt, AGENT_PERSONA
from tools.escalation import check_escalation, escalation_message, fallback_message

# ── Configuration ────────────────────────────────────────────────────────────

MODEL = "gpt-4o"
MAX_TOKENS = 120          # Voice agents must be brief
TEMPERATURE = 0.6         # Slightly creative but consistent
MAX_HISTORY_TURNS = 10    # Sliding window to manage context size
TYPING_DELAY = 0.03       # Simulated speaking pace (seconds per char)

# ── Colours (terminal) ───────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GREEN  = "\033[92m"
DIM    = "\033[2m"

# ── Helpers ──────────────────────────────────────────────────────────────────

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def stream_print(text: str, color: str = CYAN) -> None:
    """Print text character by character to simulate spoken delivery."""
    print(f"{color}{BOLD}", end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        time.sleep(TYPING_DELAY)
    print(f"{RESET}\n")


def trim_history(history: list) -> list:
    """Keep only the most recent turns to stay within context budget."""
    if len(history) > MAX_HISTORY_TURNS * 2:
        return history[-(MAX_HISTORY_TURNS * 2):]
    return history


def get_agent_response(history: list) -> str:
    """Call OpenAI and return the agent's next utterance."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": build_system_prompt()},
                *history,
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[API Error: {e}]"


def print_header() -> None:
    name = AGENT_PERSONA["name"]
    clinic = AGENT_PERSONA["clinic"]
    print(f"\n{BOLD}{GREEN}{'─' * 55}{RESET}")
    print(f"{BOLD}{GREEN}  🦷  {clinic} — AI Voice Agent Simulator{RESET}")
    print(f"{BOLD}{GREEN}{'─' * 55}{RESET}")
    print(f"{DIM}  Agent : {name}  |  Model : {MODEL}  |  Max turns in memory : {MAX_HISTORY_TURNS}{RESET}")
    print(f"{DIM}  Type  : 'quit' or 'exit' to end the session{RESET}")
    print(f"{BOLD}{GREEN}{'─' * 55}{RESET}\n")


def print_turn_divider(turn: int) -> None:
    print(f"{DIM}── Turn {turn} {'─' * 44}{RESET}")


# ── Main Loop ────────────────────────────────────────────────────────────────

def run() -> None:
    print_header()

    agent_name = AGENT_PERSONA["name"]
    history: list = []
    turn = 0

    # Opening greeting
    greeting = (
        f"Thank you for calling BrightSmile Dental Clinic, "
        f"my name is {agent_name} and I'm here to help. "
        f"How can I assist you today?"
    )
    print(f"{YELLOW}{BOLD}  {agent_name}:{RESET} ", end="")
    stream_print(greeting)

    while True:
        turn += 1
        print_turn_divider(turn)

        # ── User input ───────────────────────────────────────────────────────
        try:
            user_input = input(f"{BOLD}  You: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{DIM}Session interrupted.{RESET}\n")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye", "goodbye"):
            farewell = "Thank you for calling BrightSmile. Have a wonderful day!"
            print(f"\n{YELLOW}{BOLD}  {agent_name}:{RESET} ", end="")
            stream_print(farewell)
            break

        # ── Escalation check ─────────────────────────────────────────────────
        history.append({"role": "user", "content": user_input})
        history = trim_history(history)

        escalation = check_escalation(user_input, history)
        if escalation["escalate"]:
            reason = escalation["reason"]
            print(f"{DIM}  [ESCALATION] {reason}{RESET}")
            response = escalation_message(agent_name)
            print(f"\n{RED}{BOLD}  {agent_name} [escalating]:{RESET} ", end="")
            stream_print(response, color=RED)
            print(f"{DIM}  — Session ended: transferred to human staff —{RESET}\n")
            break

        # ── Agent response ───────────────────────────────────────────────────
        print(f"\n{DIM}  [thinking...]{RESET}", end="\r")
        response = get_agent_response(history)
        print(" " * 20, end="\r")  # Clear the thinking line

        history.append({"role": "assistant", "content": response})

        print(f"{YELLOW}{BOLD}  {agent_name}:{RESET} ", end="")
        stream_print(response)


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print(f"{RED}Error: OPENAI_API_KEY environment variable not set.{RESET}")
        sys.exit(1)
    run()
