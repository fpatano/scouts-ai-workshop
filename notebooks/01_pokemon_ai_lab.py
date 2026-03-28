# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # 🎮 Pokemon AI Lab
# MAGIC
# MAGIC Welcome, Scout! Today you're going to use **real AI** on real data.
# MAGIC
# MAGIC By the end of this lab you will:
# MAGIC - Understand what AI actually is (and isn't)
# MAGIC - Use AI functions to classify, summarize, and answer questions about Pokemon
# MAGIC - Learn how to write good prompts (prompt engineering)
# MAGIC - Think about AI ethics: bias, fairness, and deepfakes
# MAGIC
# MAGIC Let's go!

# COMMAND ----------
# MAGIC %md
# MAGIC ---
# MAGIC # Part 1: What IS Artificial Intelligence?
# MAGIC
# MAGIC **AI is pattern recognition at scale.** That's it. No magic, no thinking, no feelings.
# MAGIC
# MAGIC A Pokedex doesn't "know" what a Pikachu is. It was trained on thousands of examples until it learned
# MAGIC the pattern: yellow + mouse-shaped + electric cheeks = Pikachu.
# MAGIC
# MAGIC | Term | Pokemon Analogy | Real Definition |
# MAGIC |------|----------------|-----------------|
# MAGIC | **AI** | A Pokedex that identifies Pokemon | Software that finds patterns in data to make predictions |
# MAGIC | **Machine Learning** | Training your Pokedex by showing it 1000 Pikachu photos | AI that improves by learning from examples, not rules |
# MAGIC | **Training Data** | All the Pokemon photos you fed it | The examples an AI learns from |
# MAGIC | **Model** | The Pokedex's brain after training | The learned patterns stored as math |
# MAGIC | **Inference** | Pointing your Pokedex at a new Pokemon | Using a trained model to make a prediction |
# MAGIC | **Prompt** | What you type into the Pokedex search bar | The instruction you give an AI |
# MAGIC | **Bias** | A Pokedex trained only on Gen 1 can't recognize Gen 3 | When AI reflects gaps or unfairness in its training data |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Let's explore the data
# MAGIC
# MAGIC Before we use AI, we need to understand our data. Every good data scientist looks at the data first.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- How many Pokemon per type?
# MAGIC SELECT type_1, count(*) as count
# MAGIC FROM pokemon
# MAGIC GROUP BY type_1
# MAGIC ORDER BY count DESC

# COMMAND ----------
# MAGIC %sql
# MAGIC -- Who are the strongest Pokemon? (by base stat total)
# MAGIC SELECT name, type_1, type_2, base_stat_total, is_legendary
# MAGIC FROM pokemon
# MAGIC ORDER BY base_stat_total DESC
# MAGIC LIMIT 10

# COMMAND ----------
# MAGIC %sql
# MAGIC -- Average stats by type - which type is the "best"?
# MAGIC SELECT
# MAGIC     type_1,
# MAGIC     count(*) as count,
# MAGIC     round(avg(hp), 1) as avg_hp,
# MAGIC     round(avg(attack), 1) as avg_attack,
# MAGIC     round(avg(defense), 1) as avg_defense,
# MAGIC     round(avg(speed), 1) as avg_speed,
# MAGIC     round(avg(base_stat_total), 1) as avg_total
# MAGIC FROM pokemon
# MAGIC GROUP BY type_1
# MAGIC ORDER BY avg_total DESC

# COMMAND ----------
# MAGIC %md
# MAGIC ### What just happened?
# MAGIC
# MAGIC You just did **data exploration** using SQL (Structured Query Language). This is what data scientists
# MAGIC do every day. No AI yet! Just counting, averaging, and sorting.
# MAGIC
# MAGIC Notice anything interesting? Dragon types have the highest average stats. Water types are the most common.
# MAGIC We'll come back to this when we talk about **bias**.

# COMMAND ----------
# MAGIC %md
# MAGIC ---
# MAGIC # Part 2: AI Functions - Making AI Do Work
# MAGIC
# MAGIC Databricks has built-in AI functions you can call right from SQL. No setup, no API keys, no code.
# MAGIC You just call them like any other function.
# MAGIC
# MAGIC We're going to use three:
# MAGIC - **ai_classify()** - Sort things into categories (like a Sorting Hat)
# MAGIC - **ai_summarize()** - Write a short summary of text
# MAGIC - **ai_query()** - Ask the AI anything (free-form questions)

# COMMAND ----------
# MAGIC %md
# MAGIC ## ai_classify: The Pokemon Sorting Hat
# MAGIC
# MAGIC `ai_classify()` takes text and sorts it into categories you define.
# MAGIC Think of it like a Sorting Hat, but instead of Hogwarts houses, you pick the categories.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- Let's classify Pokemon into battle roles based on their stats
# MAGIC SELECT
# MAGIC     name,
# MAGIC     type_1,
# MAGIC     attack,
# MAGIC     defense,
# MAGIC     speed,
# MAGIC     ai_classify(
# MAGIC         concat('Pokemon with ', cast(attack as string), ' attack, ',
# MAGIC                cast(defense as string), ' defense, and ',
# MAGIC                cast(speed as string), ' speed'),
# MAGIC         ARRAY('Attacker', 'Defender', 'Speedster', 'All-Rounder')
# MAGIC     ) as battle_role
# MAGIC FROM pokemon
# MAGIC WHERE name IN ('Pikachu', 'Snorlax', 'Alakazam', 'Steelix', 'Charizard', 'Blissey', 'Mewtwo', 'Shuckle')

# COMMAND ----------
# MAGIC %md
# MAGIC ### What just happened?
# MAGIC
# MAGIC The AI read each Pokemon's stats and decided which **battle role** fits best.
# MAGIC - Pikachu has high speed -> Speedster
# MAGIC - Snorlax has high HP and defense -> Defender
# MAGIC - Mewtwo has high everything -> probably Attacker or All-Rounder
# MAGIC
# MAGIC The AI didn't memorize a lookup table. It **reasoned** about the numbers and picked the best category.
# MAGIC
# MAGIC **Think about it:** Did the AI get every classification right? Would YOU classify them differently?

# COMMAND ----------
# MAGIC %md
# MAGIC ## 🔥 TRY IT: Your own classification
# MAGIC
# MAGIC Change the categories! Try classifying Pokemon into:
# MAGIC - Your own team roles (Tank, DPS, Healer, Support)
# MAGIC - Difficulty levels (Easy to Catch, Medium, Hard to Catch)
# MAGIC - Anything you want!
# MAGIC
# MAGIC Edit the SQL below and run it.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- YOUR TURN! Change the categories in the ARRAY below
# MAGIC SELECT
# MAGIC     name,
# MAGIC     type_1,
# MAGIC     hp,
# MAGIC     attack,
# MAGIC     defense,
# MAGIC     speed,
# MAGIC     ai_classify(
# MAGIC         concat(name, ' is a ', type_1, ' type Pokemon with ',
# MAGIC                cast(hp as string), ' HP, ',
# MAGIC                cast(attack as string), ' attack, ',
# MAGIC                cast(defense as string), ' defense, ',
# MAGIC                cast(speed as string), ' speed'),
# MAGIC         ARRAY('Tank', 'DPS', 'Healer', 'Support')
# MAGIC     ) as my_role
# MAGIC FROM pokemon
# MAGIC WHERE name IN ('Pikachu', 'Charizard', 'Blastoise', 'Venusaur', 'Mewtwo', 'Eevee', 'Gengar', 'Machamp')

# COMMAND ----------
# MAGIC %md
# MAGIC ## ai_summarize: TL;DR for data
# MAGIC
# MAGIC `ai_summarize()` takes text and writes a short summary. Useful when you have
# MAGIC a lot of information and need the key points fast.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- Summarize a Pokemon's full profile
# MAGIC SELECT
# MAGIC     name,
# MAGIC     ai_summarize(
# MAGIC         concat(name, ' is a Generation ', cast(generation as string),
# MAGIC                ' Pokemon. Primary type: ', type_1,
# MAGIC                coalesce(concat(', secondary type: ', type_2), ''),
# MAGIC                '. Base stats: HP ', cast(hp as string),
# MAGIC                ', Attack ', cast(attack as string),
# MAGIC                ', Defense ', cast(defense as string),
# MAGIC                ', Sp. Attack ', cast(sp_attack as string),
# MAGIC                ', Sp. Defense ', cast(sp_defense as string),
# MAGIC                ', Speed ', cast(speed as string),
# MAGIC                '. Total: ', cast(base_stat_total as string),
# MAGIC                '. Legendary: ', cast(is_legendary as string),
# MAGIC                '. Catch rate: ', cast(catch_rate as string),
# MAGIC                '. Abilities: ', abilities),
# MAGIC         20
# MAGIC     ) as summary
# MAGIC FROM pokemon
# MAGIC WHERE name IN ('Mewtwo', 'Pikachu', 'Magikarp', 'Rayquaza')

# COMMAND ----------
# MAGIC %md
# MAGIC ### What just happened?
# MAGIC
# MAGIC We gave the AI a wall of stats and it wrote a human-readable summary in about 20 words.
# MAGIC This is what AI is great at: turning structured data into natural language.
# MAGIC
# MAGIC Notice how Magikarp's summary probably mentions it being weak. The AI understands
# MAGIC context, not just numbers.

# COMMAND ----------
# MAGIC %md
# MAGIC ## ai_query: Ask the AI anything
# MAGIC
# MAGIC `ai_query()` is the most powerful function. You write a prompt (a question or instruction)
# MAGIC and the AI gives you a free-form answer.
# MAGIC
# MAGIC This is where **prompt engineering** comes in. The better your prompt, the better the answer.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- Ask the AI to write a Pokedex entry
# MAGIC SELECT
# MAGIC     name,
# MAGIC     ai_query(
# MAGIC         'databricks-meta-llama-3-3-70b-instruct',
# MAGIC         concat('Write a fun 2-sentence Pokedex entry for a Pokemon named ', name,
# MAGIC                ' that is a ', type_1, ' type with ', cast(base_stat_total as string),
# MAGIC                ' base stat total. Make it sound like a real Pokedex entry.')
# MAGIC     ) as pokedex_entry
# MAGIC FROM pokemon
# MAGIC WHERE name IN ('Pikachu', 'Charizard', 'Snorlax', 'Gengar', 'Eevee')

# COMMAND ----------
# MAGIC %md
# MAGIC ---
# MAGIC # Part 3: Prompt Engineering
# MAGIC
# MAGIC **Prompt engineering** is the skill of writing instructions that get the AI to do what you want.
# MAGIC
# MAGIC It's like giving directions. "Go to the store" is vague. "Walk two blocks north, turn left
# MAGIC at the red building, enter the blue door" gets results.
# MAGIC
# MAGIC **Three rules for good prompts:**
# MAGIC 1. **Be specific** - Tell the AI exactly what format and length you want
# MAGIC 2. **Give context** - Include relevant facts the AI needs
# MAGIC 3. **Show examples** - If you want a specific style, show one
# MAGIC
# MAGIC Let's see the difference.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- BAD PROMPT: Vague, no format, no context
# MAGIC SELECT ai_query(
# MAGIC     'databricks-meta-llama-3-3-70b-instruct',
# MAGIC     'Tell me about Charizard'
# MAGIC ) as bad_prompt_result

# COMMAND ----------
# MAGIC %sql
# MAGIC -- GOOD PROMPT: Specific role, format, length, context
# MAGIC SELECT ai_query(
# MAGIC     'databricks-meta-llama-3-3-70b-instruct',
# MAGIC     'You are a Pokemon professor writing a field guide for young trainers.
# MAGIC      Write a 3-bullet analysis of Charizard covering:
# MAGIC      1. Best battle strategy based on its Fire/Flying typing
# MAGIC      2. One weakness trainers should watch out for
# MAGIC      3. A fun fact
# MAGIC      Keep each bullet under 20 words. Use simple language.'
# MAGIC ) as good_prompt_result

# COMMAND ----------
# MAGIC %md
# MAGIC ### See the difference?
# MAGIC
# MAGIC The bad prompt gives you a generic Wikipedia-style dump.
# MAGIC The good prompt gives you exactly what you asked for: 3 short bullets, written for kids, focused on battle.
# MAGIC
# MAGIC **The AI is equally smart both times.** The difference is entirely in your prompt.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 🔥 TRY IT: The Prompt Challenge
# MAGIC
# MAGIC Pick your favorite Pokemon and write a prompt that gets the AI to:
# MAGIC 1. Analyze its competitive strengths and weaknesses
# MAGIC 2. Suggest a 3-Pokemon team that covers its weaknesses
# MAGIC 3. Keep the whole response under 100 words
# MAGIC
# MAGIC **Hint:** Tell the AI what role to play (trainer, professor, analyst). Give it the stats. Specify the format.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- YOUR TURN! Write your prompt below
# MAGIC -- Replace the text inside the quotes
# MAGIC SELECT ai_query(
# MAGIC     'databricks-meta-llama-3-3-70b-instruct',
# MAGIC     'You are a competitive Pokemon trainer.
# MAGIC      Analyze [YOUR POKEMON HERE] and suggest a 3-Pokemon team
# MAGIC      that covers its weaknesses. Keep it under 100 words.'
# MAGIC ) as my_prompt_result

# COMMAND ----------
# MAGIC %md
# MAGIC ## Combining AI with data
# MAGIC
# MAGIC The real power comes when you combine AI functions with your data.
# MAGIC Here we ask the AI to analyze the ACTUAL stats from our table.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- AI-powered team builder: find the best partner for any Pokemon
# MAGIC SELECT
# MAGIC     name,
# MAGIC     type_1,
# MAGIC     type_2,
# MAGIC     base_stat_total,
# MAGIC     ai_query(
# MAGIC         'databricks-meta-llama-3-3-70b-instruct',
# MAGIC         concat('In one sentence, what type of Pokemon would be the best battle partner for ',
# MAGIC                name, ' who is ', type_1,
# MAGIC                coalesce(concat('/', type_2), ''),
# MAGIC                ' type? Consider type coverage only.')
# MAGIC     ) as best_partner_type
# MAGIC FROM pokemon
# MAGIC WHERE name IN ('Charizard', 'Blastoise', 'Venusaur', 'Pikachu', 'Gengar')

# COMMAND ----------
# MAGIC %md
# MAGIC ---
# MAGIC # Part 4: AI Ethics - The Hard Questions
# MAGIC
# MAGIC AI is powerful. But powerful tools need responsible users. Let's talk about three
# MAGIC things every Scout should know.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Bias in AI
# MAGIC
# MAGIC Remember how we saw that Dragon types have the highest average stats? What if someone
# MAGIC built a "Best Pokemon Recommender" AI trained only on base stats?
# MAGIC
# MAGIC It would ALWAYS recommend Dragon and Legendary Pokemon. It would never suggest Pikachu
# MAGIC or Eevee, even though those might be perfect for a beginning trainer.
# MAGIC
# MAGIC **That's bias.** The AI isn't wrong about the numbers. But it's missing context that matters:
# MAGIC fun, availability, personal preference, catch difficulty.
# MAGIC
# MAGIC Real-world examples of AI bias:
# MAGIC - Facial recognition that works worse on darker skin (training data was mostly light-skinned faces)
# MAGIC - Resume screening AI that penalized women (trained on historically male-dominated hiring data)
# MAGIC - Loan approval AI that discriminated by zip code (zip codes correlate with race)

# COMMAND ----------
# MAGIC %sql
# MAGIC -- BIAS DEMO: If we only look at stats, we get a biased "best Pokemon" list
# MAGIC SELECT name, type_1, base_stat_total, is_legendary,
# MAGIC     CASE
# MAGIC         WHEN is_legendary = true THEN '(Legendary - most trainers will never catch this)'
# MAGIC         WHEN catch_rate < 45 THEN '(Very rare - hard to find)'
# MAGIC         ELSE '(Available to most trainers)'
# MAGIC     END as reality_check
# MAGIC FROM pokemon
# MAGIC ORDER BY base_stat_total DESC
# MAGIC LIMIT 10

# COMMAND ----------
# MAGIC %md
# MAGIC ### The lesson
# MAGIC
# MAGIC 9 out of 10 "best" Pokemon are legendary or mega evolutions. A stats-only AI would recommend
# MAGIC Pokemon that most trainers can never actually get. **Data without context creates unfair results.**
# MAGIC
# MAGIC When you build or use AI, always ask: **Who is missing from this data? Who could this hurt?**

# COMMAND ----------
# MAGIC %md
# MAGIC ## Deepfakes and AI-Generated Content
# MAGIC
# MAGIC AI can generate text, images, and videos that look real but aren't.
# MAGIC Let's see how easy it is to generate convincing fake content.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- The AI can generate totally fake but convincing Pokemon lore
# MAGIC SELECT ai_query(
# MAGIC     'databricks-meta-llama-3-3-70b-instruct',
# MAGIC     'Write a short, convincing fake news article (3 sentences) claiming that
# MAGIC      scientists discovered a real animal that looks exactly like Pikachu in the
# MAGIC      Amazon rainforest. Make it sound like a real BBC news article.
# MAGIC      Then add a line that says: "[This is AI-generated and not real]"'
# MAGIC ) as fake_news_demo

# COMMAND ----------
# MAGIC %md
# MAGIC ### That looked pretty real, right?
# MAGIC
# MAGIC That's the problem. AI can generate convincing fake text in seconds. The same technology
# MAGIC can create fake images and videos (deepfakes).
# MAGIC
# MAGIC **How to protect yourself:**
# MAGIC 1. **Check the source** - Is it from a known, trusted news outlet?
# MAGIC 2. **Look for verification** - Can you find the same story from multiple sources?
# MAGIC 3. **Be skeptical of perfect** - Real photos have imperfections. AI-generated images often look too clean.
# MAGIC 4. **Check the date and context** - Old images get reused with new fake stories.
# MAGIC
# MAGIC **Scout Honor principle:** Just because you CAN generate fake content doesn't mean you should.
# MAGIC AI should be used to help people, not deceive them.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Three Ethics Rules for AI Users
# MAGIC
# MAGIC 1. **Transparency** - Always tell people when content is AI-generated
# MAGIC 2. **Fairness** - Check your data for bias before trusting AI recommendations
# MAGIC 3. **Accountability** - You are responsible for how you use AI, not the AI itself

# COMMAND ----------
# MAGIC %md
# MAGIC ---
# MAGIC # Part 5: Final Challenge
# MAGIC
# MAGIC Put everything together! Use `ai_query()` to build something useful with the Pokemon data.
# MAGIC
# MAGIC **Ideas:**
# MAGIC - A Pokemon team recommender for a specific strategy
# MAGIC - A "Pokemon of the Day" generator that writes a fun fact
# MAGIC - A difficulty rating system for catching each Pokemon
# MAGIC - A Pokemon matchup analyzer (who would win?)
# MAGIC
# MAGIC Use the empty cell below. Look back at the examples above for syntax.

# COMMAND ----------
# MAGIC %sql
# MAGIC -- YOUR FINAL CHALLENGE! Build something cool.
# MAGIC -- Here's a starter template - modify it however you want:
# MAGIC SELECT
# MAGIC     name,
# MAGIC     type_1,
# MAGIC     base_stat_total,
# MAGIC     ai_query(
# MAGIC         'databricks-meta-llama-3-3-70b-instruct',
# MAGIC         concat('YOUR PROMPT HERE about ', name)
# MAGIC     ) as ai_result
# MAGIC FROM pokemon
# MAGIC WHERE name IN ('Pikachu', 'Charizard', 'Mewtwo')

# COMMAND ----------
# MAGIC %md
# MAGIC ---
# MAGIC # You did it!
# MAGIC
# MAGIC Today you:
# MAGIC - Explored real data using SQL
# MAGIC - Used AI to classify, summarize, and generate text
# MAGIC - Learned prompt engineering (specific > vague)
# MAGIC - Discussed bias, deepfakes, and AI ethics
# MAGIC
# MAGIC **Merit Badge Requirements Covered:**
# MAGIC - Req 1: Key AI concepts (machine learning, training data, models, inference)
# MAGIC - Req 2: AI basics (how AI learns from data, pattern recognition)
# MAGIC - Req 4: Ethics (bias, deepfakes, transparency, fairness, accountability)
# MAGIC - Req 6: Prompt engineering (good vs bad prompts, specific instructions)
# MAGIC - Req 7: Practical application (hands-on with real AI functions)
# MAGIC
# MAGIC **Keep exploring!** Your Free Edition workspace stays active. Come back and try more queries anytime.
