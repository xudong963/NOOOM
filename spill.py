import argparse
import os
from pathlib import Path
import re
import subprocess


def execute_sql(query):
    """Execute an SQL query using bendsql and check for 'APIError: ResponseError'."""
    command = ["bendsql", "--query=" + query, "--time=server"]
    result = subprocess.run(command, text=True, capture_output=True)

    # Check for 'APIError: ResponseError' in stderr
    if "APIError: ResponseError" in result.stderr:
        raise RuntimeError(
            f"'APIError: ResponseError' found in bendsql output: {result.stderr}"
        )
    elif result.returncode != 0:
        # Handle other types of errors
        raise RuntimeError(
            f"bendsql command failed with return code {result.returncode}: {result.stderr}"
        )

    return result.stdout


def extract_time(output):
    """Extract execution time from the bendsql output."""
    match = re.search(r"([0-9.]+)$", output)
    if not match:
        raise ValueError("Could not extract time from output.")
    return match.group(1)


def main():
    parser = argparse.ArgumentParser(
        description="Execute SQL queries on limited memery to test databend spilling capability"
    )
    parser.add_argument("--ratio", default=0)
    parser.add_argument("--database", default=None, required=True)

    args = parser.parse_args()

    # Before runing sqls, set the memory limit by ratio
    execute_sql(f"set join_spilling_memory_ratio = {args.ratio};")
    execute_sql(f"use {args.database};")

    dir = "queries/"
    # Read the SQL files in `queries` directory
    for file in os.listdir(dir):
        if file.endswith(".sql"):
            with open(Path(dir + file), "r") as f:
                content = f.read()
                queries = [
                    query.strip() for query in content.split(";") if query.strip()
                ]
                # Execute the SQL
                for query in queries:
                    # print the query and its file name
                    print(f"Executing query: {query} from file: {file}")
                    output = execute_sql(query)
                    print(f"Time elapsed: {extract_time(output)} seconds\n")


if __name__ == "__main__":
    main()
