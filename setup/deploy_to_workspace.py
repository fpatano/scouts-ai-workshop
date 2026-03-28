"""
Deploy the Scouts AI Workshop to a Databricks workspace.

Run once before the workshop (or once per Scout workspace).
Reads DATABRICKS_HOST and DATABRICKS_TOKEN from environment or .env file.

Usage:
    cd scouts-ai-workshop/setup
    cp .env.example .env   # edit with your values
    pip install -r requirements.txt
    python deploy_to_workspace.py
"""

import os
import sys

# Load .env if present
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat
from databricks.sdk.service.catalog import VolumeType

def main():
    w = WorkspaceClient()

    # Who are we?
    user = w.current_user.me().user_name
    print(f"Deploying as: {user}")

    # Detect workspace catalog
    # On Free Edition the default catalog is usually "workspace"
    catalogs = [c.name for c in w.catalogs.list() if c.name not in ("system", "samples", "__databricks_internal")]
    if "workspace" in catalogs:
        catalog = "workspace"
    else:
        catalog = catalogs[0] if catalogs else "main"
    print(f"Using catalog: {catalog}")

    # Workspace folder
    workshop_dir = f"/Workspace/Users/{user}/scouts-ai-workshop"
    print(f"Uploading notebooks to: {workshop_dir}")

    notebooks_dir = os.path.join(os.path.dirname(__file__), "..", "notebooks")
    for nb_file in sorted(os.listdir(notebooks_dir)):
        if not nb_file.endswith(".py"):
            continue
        nb_path = f"{workshop_dir}/{nb_file}"
        with open(os.path.join(notebooks_dir, nb_file), "rb") as f:
            w.workspace.upload(nb_path, f, format=ImportFormat.AUTO, overwrite=True)
        print(f"  Uploaded: {nb_file}")

    # Create volume for data
    volume_name = "workshop_data"
    try:
        w.volumes.create(
            catalog_name=catalog,
            schema_name="default",
            name=volume_name,
            volume_type=VolumeType.MANAGED
        )
        print(f"Created volume: {catalog}.default.{volume_name}")
    except Exception:
        print(f"Volume {catalog}.default.{volume_name} already exists")

    # Upload CSV
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pokemon.csv")
    volume_file_path = f"/Volumes/{catalog}/default/{volume_name}/pokemon.csv"
    with open(csv_path, "rb") as f:
        w.files.upload(volume_file_path, f, overwrite=True)
    print(f"Uploaded pokemon.csv to {volume_file_path}")

    # Done
    host = os.environ.get("DATABRICKS_HOST", w.config.host).rstrip("/")
    print(f"\nDone! Open your workshop folder:")
    print(f"  {host}/#workspace{workshop_dir}")
    print(f"\nScouts should open 00_setup.py first and click Run All.")

if __name__ == "__main__":
    main()
