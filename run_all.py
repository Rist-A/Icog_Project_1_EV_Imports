#!/usr/bin/env python3

import argparse
import ast
import json
import os
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOKS = ROOT / "notebooks"
STEPS = [
    ("00a", "Select the vehicles (Adey Market + Gezat evidence, ranking of the 5 candidates)", "Wubrist_Alemu_00a_select_vehicles.ipynb"),
    ("00", "Collect part evidence (scraper)", "Wubrist_Alemu_00_collect_evidence.ipynb"),
    ("01", "Clean and validate the evidence sheet", "Wubrist_Alemu_01_clean_data.ipynb"),
    ("02", "Score, rank and test the ranking", "Wubrist_Alemu_02_scoring_ranking.ipynb"),
]

HINTS = {
    "FileNotFoundError": "A file is missing. Run the earlier step first (00 creates the sheet that 01 reads, 01 creates the file that 02 reads).",
    "AssertionError": "A safety check stopped the run. Read the message above: it says what to fix.",
    "ModuleNotFoundError": "A library is missing. Run:  pip install -r requirements.txt",
    "ConnectionError": "No internet connection. Connect, or run with --skip-collect to use the files already saved.",
}


def cells_of(path):
    nb = json.loads(path.read_text(encoding="utf-8"))
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def show_last_expression(source, filename):
    # In a notebook the last line of a cell is displayed automatically. A script does not do that,
    # so print it, to give the same output you would see in Jupyter.
    tree = ast.parse(source, filename)
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        value = tree.body[-1].value
        is_print = isinstance(value, ast.Call) and getattr(value.func, "id", "") == "print"
        if not is_print:
            tree.body[-1] = ast.Expr(ast.Call(ast.Name("print", ast.Load()), [value], []))
            ast.fix_missing_locations(tree)
    return compile(tree, filename, "exec")


def run_notebook(path):
    namespace = {"__name__": "__main__", "__file__": str(path)}
    for number, source in enumerate(cells_of(path), start=1):
        try:
            exec(show_last_expression(source, f"{path.name} (code cell {number})"), namespace)
        except Exception as error:
            print("\n" + "=" * 70)
            print(f"STOPPED in {path.name}, code cell {number}")
            print(f"{type(error).__name__}: {error}")
            hint = next((h for k, h in HINTS.items() if k in type(error).__name__), None)
            if hint:
                print("Hint:", hint)
            print("=" * 70)
            traceback.print_exc(limit=3)
            raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description="Run the whole project with one command.")
    parser.add_argument("--email", help="your real email address (sent to websites as a contact)")
    parser.add_argument("--skip-collect", action="store_true", help="offline mode: contact no website")
    parser.add_argument("--only", choices=["00a", "00", "01", "02"], help="run only one step")
    parser.add_argument("--keep-going", action="store_true", help="continue even if a step fails")
    args = parser.parse_args()

    os.environ.setdefault("MPLBACKEND", "Agg")          # draw charts to files, no pop-up windows
    try:
        import pandas as pd
        pd.set_option("display.width", 200)
        pd.set_option("display.max_columns", 40)
    except ImportError:
        print("pandas is not installed. Run:  pip install -r requirements.txt")
        return 1

    if args.email:
        os.environ["SCRAPER_CONTACT_EMAIL"] = args.email

    steps = [s for s in STEPS if (args.only is None or s[0] == args.only)]
    if args.skip_collect:
        os.environ["RUN_OFFLINE"] = "1"                 # no website is contacted
        steps = [s for s in steps if s[0] != "00"]
    web_steps = [s for s in steps if s[0] in ("00a", "00")] if not args.skip_collect else []
    if web_steps and not os.environ.get("SCRAPER_CONTACT_EMAIL"):
        print("The web steps visit websites, so they need a real contact email. Run it like this:")
        print("    python run_all.py --email you@example.com")
        print("(or add --skip-collect to work offline from the files you already have)")
        return 2

    print(f"Project folder: {ROOT}")
    started = time.time()
    failed = []
    for step_id, title, filename in steps:
        print("\n" + "#" * 70 + f"\n# STEP {step_id}: {title}\n" + "#" * 70)
        t0 = time.time()
        try:
            run_notebook(NOTEBOOKS / filename)
            print(f"\n-> step {step_id} finished in {time.time() - t0:.0f}s")
        except SystemExit:
            failed.append(step_id)
            if not args.keep_going:
                print(f"\nStopped at step {step_id}. Fix the problem above, then run the same command again.")
                return 1

    print("\n" + "=" * 70)
    print(f"DONE in {time.time() - started:.0f}s" + (f" (steps with problems: {failed})" if failed else ""))
    top5 = ROOT / "data" / "processed" / "top5_parts.csv"
    if top5.exists():
        import pandas as pd
        table = pd.read_csv(top5)
        ranking = pd.read_csv(ROOT / "data" / "processed" / "part_ranking.csv")
        if ranking["score"].nunique() == 1:
            print("\nWARNING: all parts have the same score, so there is almost no evidence yet.")
            print("This is NOT a real recommendation. Collect the evidence and fill in the sheet first (see README).")
        else:
            print("\nThe five recommended parts (data/processed/top5_parts.csv):")
            print(table[["rank", "part", "score", "vehicles_with_fitment_evidence", "coverage_pct"]].round(3).to_string(index=False))
    print("\nVehicle evidence: data/processed/vehicle_selection.csv  |  results: data/processed/  |  charts: figure/")
    print("Logs: data/raw/source_log.csv, fetch_log.csv")
    print("Remember: Gezat catalogue, wear_item and local_sellers are YOUR hand-collected inputs (see README).")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
