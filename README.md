# support-bot

Bilingual (Hebrew/English) customer support chatbot that runs in the terminal. Uses Claude AI for intelligent responses and persists conversation history to JSON.

## What it does

- Interactive chat interface with rich terminal formatting
- Automatic language detection — respond in Hebrew (עברית) or English
- Conversation memory — every session is saved and can be resumed later
- Session management — list past conversations, view history, resume any session

## Install

```bash
cd support-bot
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage

```bash
# Start a new conversation
python main.py

# Resume a past session
python main.py --resume 20260309_143022
```

### In-chat commands

| Command | Action |
|---------|--------|
| `/history` | View current session's full conversation |
| `/sessions` | List all past sessions |
| `/quit` | End the conversation |
| `Ctrl+C` | Exit immediately |

## Example

```
┌─── Support Bot ─────────────────────┐
│ Bilingual Support Bot               │
│ English & Hebrew | עברית ואנגלית     │
│                                     │
│ Type your question in either language│
│ Commands: /history, /sessions, /quit │
└─────────────────────────────────────┘

You → How do I reset my password?

┌──────────────────────────────────────┐
│ To reset your password:              │
│                                      │
│ 1. Go to the login page              │
│ 2. Click "Forgot Password"           │
│ 3. Enter your registered email       │
│ 4. Check your inbox for the reset    │
│    link (check spam if needed)       │
│ 5. Create a new password (min 8      │
│    characters, include a number)     │
│                                      │
│ If you don't receive the email       │
│ within 5 minutes, contact us at      │
│ support@company.com                  │
└──────────────────────────────────────┘

You → ?אפשר גם בעברית

┌──────────────────────────────────────┐
│ !בטח                                 │
│                                      │
│ :לאיפוס סיסמה                        │
│ לדף ההתחברות לכו .1                  │
│ "שכחתי סיסמה" על לחצו .2             │
│ ...                                  │
└──────────────────────────────────────┘
```

## Conversation Storage

Sessions are saved as JSON in `conversations/`:

```json
{
  "session_id": "20260309_143022",
  "created_at": "2026-03-09T14:30:22",
  "messages": [
    {
      "role": "user",
      "content": "How do I reset my password?",
      "timestamp": "2026-03-09T14:30:45"
    },
    {
      "role": "assistant",
      "content": "To reset your password:\n1. Go to...",
      "timestamp": "2026-03-09T14:30:48"
    }
  ]
}
```

## Project Structure

```
support-bot/
├── main.py           # CLI entry point and chat interface
├── bot.py            # Claude API conversation handler
├── memory.py         # JSON conversation persistence
├── conversations/    # Auto-created session storage
├── requirements.txt  # Python dependencies
└── README.md
```
