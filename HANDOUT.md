# Pokemon AI Workshop - Take Home

## AI Vocabulary

| Term | What It Means | Pokemon Example |
|------|--------------|-----------------|
| Artificial Intelligence | Software that finds patterns in data | A Pokedex that identifies Pokemon from photos |
| Machine Learning | AI that learns from examples | Training the Pokedex with 1000 Pikachu photos |
| Training Data | The examples AI learns from | All the Pokemon photos and stats |
| Model | The patterns the AI learned | The Pokedex's "brain" after training |
| Inference | Using the model to make a prediction | Pointing the Pokedex at a new Pokemon |
| Prompt | The instruction you give an AI | "Classify this Pokemon as Attacker or Defender" |
| Bias | Unfairness from incomplete data | A Pokedex trained only on Gen 1 fails on Gen 3 |

## Prompt Engineering Cheat Sheet

**Bad prompt:** "Tell me about Charizard"

**Good prompt:** "You are a Pokemon professor. Write 3 bullet points about Charizard's battle strategy, covering type advantages, one weakness, and a fun fact. Keep each bullet under 20 words."

### The Formula
1. **Role** - Tell the AI who it is ("You are a...")
2. **Task** - What exactly to do ("Write 3 bullets about...")
3. **Context** - Give it the facts it needs
4. **Format** - How to structure the answer ("Keep each under 20 words")

## AI Ethics - Three Rules

1. **Transparency** - Always say when something is AI-generated
2. **Fairness** - Check data for bias before trusting AI results
3. **Accountability** - You are responsible for how you use AI

## Questions to Ask About Any AI System

- What data was it trained on? Who is missing?
- Could this AI treat some people unfairly?
- Am I being transparent about using AI?
- Would I be comfortable if everyone could see how I'm using this?

## Keep Learning

- **Your Databricks workspace** stays active. Log back in and experiment anytime.
- **Databricks Free Edition:** https://signup.databricks.com
- **AI Merit Badge full requirements:** https://www.scouting.org/merit-badges/artificial-intelligence/
- **Prompt engineering guide:** https://docs.databricks.com/en/large-language-models/ai-functions.html

## AI Functions You Used Today

```sql
-- Classify into categories
ai_classify(text, ARRAY('Category1', 'Category2'))

-- Summarize text
ai_summarize(text, max_words)

-- Ask anything
ai_query('model-name', 'your prompt here')
```
