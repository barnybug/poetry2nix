#!/usr/bin/env python
# Patch out special dependencies (git and path) from a pyproject.json file

import argparse
import json
import sys


def main(input, output, fields_to_remove):
    data = json.load(input)

    try:
        deps = data["tool"]["poetry"]["dependencies"]
    except KeyError:
        pass
    else:
        for dep_name, dep in deps.items():
            if isinstance(dep, dict):
                removed = 0
                for field in fields_to_remove:
                    removed += dep.pop(field, None) is not None
                if removed:
                    dep["version"] = "*"

    json.dump(data, output, separators=(",", ":"))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "-i",
        "--input",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Location from which to read input JSON",
    )
    p.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Location to write output JSON",
    )
    p.add_argument(
        "-f",
        "--fields-to-remove",
        nargs="+",
        help="The fields to remove from the TOML",
    )

    args = p.parse_args()
    main(args.input, args.output, args.fields_to_remove)
