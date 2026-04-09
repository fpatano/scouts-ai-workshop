# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # 🎮 Pokemon AI Workshop - Setup
# MAGIC Run this notebook **once** to load the Pokemon data.
# MAGIC
# MAGIC Click **Run All** above and wait about 2 minutes!

# COMMAND ----------
# Detect your workspace catalog automatically
workspace_catalog = spark.sql("SELECT current_catalog()").first()[0]
print(f"Using catalog: {workspace_catalog}")

# COMMAND ----------
import os, shutil

# Derive the repo root from this notebook's path, then copy pokemon.csv into the volume
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = os.path.dirname(os.path.dirname(notebook_path))  # up from notebooks/
csv_source = f"/Workspace{repo_root}/data/pokemon.csv"
csv_dest   = f"/Volumes/{workspace_catalog}/default/workshop_data/pokemon.csv"

# Create the volume if it doesn't already exist
spark.sql(f"CREATE VOLUME IF NOT EXISTS {workspace_catalog}.default.workshop_data")
print("✓ Volume ready")

# Copy the CSV from the repo into the volume
shutil.copy(csv_source, csv_dest)
print(f"✓ Copied pokemon.csv to volume")

# COMMAND ----------
# Create Delta table from CSV in Volume
# read_files handles header detection and type inference automatically
spark.sql(f"""
    CREATE OR REPLACE TABLE {workspace_catalog}.default.pokemon
    AS SELECT * FROM read_files(
        '/Volumes/{workspace_catalog}/default/workshop_data/pokemon.csv',
        format => 'csv',
        header => true,
        inferSchema => true
    )
""")
row_count = spark.sql("SELECT count(*) FROM pokemon").first()[0]
print(f"Loaded {row_count} Pokemon into Delta table!")

# COMMAND ----------
# MAGIC %sql
# MAGIC -- Verify: you should see ~389 Pokemon
# MAGIC SELECT count(*) as total_pokemon FROM pokemon

# COMMAND ----------
# MAGIC %sql
# MAGIC -- Quick peek at some fan favorites
# MAGIC SELECT name, type_1, type_2, hp, attack, defense, speed, base_stat_total, is_legendary
# MAGIC FROM pokemon
# MAGIC WHERE name IN ('Pikachu', 'Charizard', 'Mewtwo', 'Eevee', 'Snorlax')
# MAGIC ORDER BY base_stat_total DESC

# COMMAND ----------
# MAGIC %md
# MAGIC ## You're all set!
# MAGIC
# MAGIC If you see 5 Pokemon above, your data is loaded. Close this notebook and open **01_pokemon_ai_lab**.
