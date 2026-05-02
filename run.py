#!/usr/bin/env python3

import argparse
import json
import subprocess
import tempfile
import os
from pathlib import Path


# Change these
TEMPLATE_JSON = Path("elastic.json")
OUTPUT_ROOT = Path("/home/teseo/scratch/prism/results")
EXECUTABLE = "/home/teseo/scratch/polyfem/build/PolyFEM_bin"


def folder_name_for_mesh(mesh_path: Path) -> str:
    return mesh_path.parent.name


def make_json_data(mesh_path: Path) -> dict:
    mesh_path = mesh_path.resolve()
    name = folder_name_for_mesh(mesh_path)

    with open(TEMPLATE_JSON, "r") as f:
        data = json.load(f)

    data["geometry"]["mesh"] = str(mesh_path)

    out_dir = OUTPUT_ROOT
    out_dir.mkdir(parents=True, exist_ok=True)

    data["output"]["json"] = str(out_dir / f"{name}.json")

    return data


def run_single(mesh_path: Path):
    data = make_json_data(mesh_path)

    # Create temp file manually (safer across platforms/HPC)
    fd, temp_path = tempfile.mkstemp(suffix=".json", prefix="polyfem_")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=4)

        cmd = [
            EXECUTABLE,
            "-j",
            temp_path,
        ]

        subprocess.run(cmd, check=True)

    finally:
        os.remove(temp_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("txt", type=Path)
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    args = parser.parse_args()

    with open(args.txt, "r") as f:
        mesh_paths = [Path(line.strip()) for line in f if line.strip()]

    n = len(mesh_paths)

    if "SLURM_ARRAY_TASK_ID" in os.environ:
        task_id = int(os.environ["SLURM_ARRAY_TASK_ID"])
        task_count = int(os.environ["SLURM_ARRAY_TASK_COUNT"])

        start = (task_id * n) // task_count
        end = ((task_id + 1) * n) // task_count
    else:
        if args.start is None or args.end is None:
            raise RuntimeError("Not in SLURM array: provide --start and --end")

        start = max(0, args.start)
        end = min(n, args.end)

    selected = mesh_paths[start:end]

    print(f"Running {len(selected)} meshes: [{start}, {end})")

    for mesh_path in selected:
        print(f"Running {mesh_path}", flush=True)
        run_single(mesh_path)


if __name__ == "__main__":
    main()