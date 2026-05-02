from pathlib import Path

def collect_msh_files(root_dir, output_file):
    root = Path(root_dir).resolve()
    msh_files = root.glob("**/*.msh")

    with open(output_file, "w") as f:
        for path in msh_files:
            f.write(str(path.resolve()) + "\n")

if __name__ == "__main__":
    root = "/home/zhouyuan/scratch/simulation_data"
    out = "all_meshes.txt"

    collect_msh_files(root, out)
    print(f"Saved list to {out}")