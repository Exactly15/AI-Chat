# 🦷 Voice Agent Simulator

A terminal-based simulator that replicates the prompt architecture and conversation patterns of voice AI agents built on platforms like **Retell AI** and **ElevenLabs** — including persona consistency, multi-turn memory management, fallback logic, and escalation handling.

Built with Python and OpenAI GPT-4o.

---

## Why This Exists

Real voice agents are more than chatbots. They must:
- Stay in character across unpredictable conversations
- Produce short, spoken-language responses (not markdown walls)
- Know when they're out of depth and hand off to a human
- Handle hostile, confused, or off-topic users gracefully

This project simulates that full system in Python — with versioned prompt engineering, a rule-based escalation layer, and a prompt stress test suite.

---

## Demo

```
─────────────────────────────────────────────────────
  🦷  BrightSmile Dental Clinic — AI Voice Agent Simulator
─────────────────────────────────────────────────────
  Agent : Aria  |  Model : gpt-4o  |  Max turns in memory : 10

  Aria: Thank you for calling BrightSmile Dental Clinic, my name
        is Aria and I'm here to help. How can I assist you today?

── Turn 1 ───────────────────────────────────────────
  You: I'd like to book an appointment for next Tuesday.

  Aria: I'd be happy to help you schedule that! Could I get your
        name and whether you prefer a morning or afternoon slot?

── Turn 2 ───────────────────────────────────────────
  You: I want to speak to a real person right now.

  [ESCALATION TRIGGERED] Hard trigger detected: 'real person'

  Aria [escalating]: I understand, and I'm sorry I haven't been
       able to fully help. Let me connect you with a member of
       our team who can assist you directly — please hold for
       just a moment.

  — Session ended: transferred to human staff —
```

---

## Project Structure

```
voice-agent-simulator/
├── agent.py                  # Core multi-turn conversation loop
├── requirements.txt
├── prompts/
│   └── system_prompt.py      # Versioned persona & voice constraints
├── tools/
│   └── escalation.py         # Escalation & fallback detection logic
└── tests/
    ├── demo.py               # Pre-scripted demo conversation
    └── test_turns.py         # Prompt stress tester (10 test cases)
```

---

## Key Prompt Engineering Decisions

### 1. Voice-optimised response constraints
Unlike a standard chatbot, voice agents must sound natural when spoken aloud. The system prompt enforces:
- Maximum **2 sentences per turn**
- No markdown, bullet points, or lists
- Contractions encouraged for natural speech rhythm
- One question per turn maximum

### 2. Versioned system prompts
Prompts are structured as versioned Python modules (`PROMPT_VERSION = "1.2.0"`) with clearly separated sections for persona, capabilities, limitations, voice constraints, escalation rules, and fallback rules. This makes prompt iteration auditable — not just vibes.

### 3. Sliding context window
Conversation history is trimmed to the last `MAX_HISTORY_TURNS` turns before each API call. This prevents context overflow on long sessions while maintaining conversational coherence.

### 4. Two-layer escalation system
Escalation is handled **before** the LLM call, not by the LLM itself:
- **Hard triggers**: keyword phrases → immediate escalation
- **Frustration signals**: semantic markers counted per turn
- **Repetition detection**: if user turns are suspiciously similar over N turns, escalate

This keeps escalation deterministic and testable — not dependent on model mood.

### 5. Prompt stress testing
`tests/test_turns.py` runs 10 adversarial test cases covering:
- Normal requests
- Out-of-scope questions
- Hostile language
- Prompt injection attempts
- Gibberish input
- Emotionally distressed users

Each case checks escalation correctness, response length compliance, and persona consistency.

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/voice-agent-simulator
cd voice-agent-simulator
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
```

**Live conversation:**
```bash
python agent.py
```

**Pre-scripted demo:**
```bash
python tests/demo.py
```

**Stress test suite:**
```bash
python tests/test_turns.py
```

---

## Extending This

| What to change | Where |
|---|---|
| Agent persona, name, clinic | `prompts/system_prompt.py` |
| Escalation keywords | `tools/escalation.py` |
| Response length limits | `agent.py` → `MAX_TOKENS`, `MAX_RESPONSE_WORDS` |
| Test cases | `tests/test_turns.py` → `TEST_CASES` |
| Switch to Claude / Gemini | `agent.py` → swap `client` and `get_agent_response()` |

---

## Concepts Demonstrated

- Multi-turn conversation history management
- Voice-optimised prompt design (Retell AI / ElevenLabs conventions)
- Deterministic escalation logic (rule-based, not LLM-dependent)
- Prompt versioning and structured system prompt architecture
- Adversarial prompt stress testing
- Context window management with sliding history window
- Prompt injection resistance

---

## License

MIT
