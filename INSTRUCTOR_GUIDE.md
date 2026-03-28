# Instructor Guide

## Before the Workshop

### 1 week before
- Create your own Databricks Free Edition account and test all notebooks end-to-end
- Print HANDOUT.md (one per Scout)
- Send Scouts signup instructions: https://signup.databricks.com

### Day of
- Arrive 30 min early to test wifi
- Have the deploy script ready (Option A) or repo URL on the board (Option B)
- Each Scout should already have a workspace. If not, budget 10 min for signup.

## Timing Guide

| Clock | Section | What's happening | Instructor action |
|-------|---------|-----------------|-------------------|
| 0:00 | Welcome | Scouts log in | Help with login issues |
| 0:10 | Setup | Run 00_setup.py | Walk around, confirm 389 Pokemon |
| 0:15 | Part 1 | AI vocab + data exploration | Talk through the vocab table. Ask: "What patterns do you see?" |
| 0:25 | Part 2 | AI functions | Live demo ai_classify first, then let them try |
| 0:35 | Part 2 | TRY IT sections | Circulate. Help with SQL syntax. |
| 0:40 | Part 3 | Prompt engineering | Show bad vs good prompt side by side. Big reaction moment. |
| 0:45 | Part 4 | Ethics | This is discussion time. Slow down. Ask questions. |
| 0:50 | Part 5 | Final challenge | Let them freestyle. Share cool results. |
| 0:55 | Wrap | Recap + handouts | Distribute HANDOUT.md printouts |

## Talking Points

### Part 1: What is AI?
- "AI doesn't think. It finds patterns. Your brain does this too, but differently."
- "When you see a Pikachu plushie and know it's Pikachu, your brain is doing inference."
- Point at the type distribution chart: "Water is most common. If I trained an AI only on type counts, it would think every Pokemon is Water type. That's bias."

### Part 2: AI Functions
- "These functions are running on a real AI model right now. Same technology as ChatGPT."
- When ai_classify runs: "Did it get them all right? What would YOU change?"
- "The AI doesn't have a Pokemon database in its head. It's reasoning from the text we gave it."

### Part 3: Prompt Engineering
- "This is the #1 most valuable skill in AI right now."
- Show the bad prompt, then the good prompt. Let the contrast speak.
- "The AI didn't get smarter. YOU got smarter at asking."

### Part 4: Ethics
- "Look at the top 10 Pokemon list. 9 are legendary. Is that fair?"
- "If a company used an AI like this to hire people, and the training data was biased, who gets hurt?"
- The deepfake demo is intentionally unsettling. Let them sit with it.
- "A Scout is trustworthy. How does that apply to AI?"

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No warehouse found" | The Serverless Starter Warehouse should auto-start. Wait 30 sec and retry. |
| AI function returns error | Warehouse may be cold-starting. Wait 1 min, run again. |
| "Table not found" | Scout didn't run 00_setup. Go back and run it. |
| CSV not found | If using Git Folder path, make sure the data/ folder is in the repo root. |
| Slow AI responses | Free Edition has rate limits. Keep to <10 rows per AI function call. |
| Scout can't sign up | Need a personal email (not school). Gmail works. Must be 13+ for account. |
| Notebook won't attach | Click "Connect" in top-right, select the Serverless option. |
