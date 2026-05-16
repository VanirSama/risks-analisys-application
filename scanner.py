import pathlib


def draw_tree(directory, prefix=""):
    paths = sorted(list(directory.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
    count = len(paths)
    exclude = ["__pycache__", ".venv", ".idea", "scanner.py"]

    for i, path in enumerate(paths):

        if path.name in exclude:
            continue

        def is_last(index: int):
            return index == count - 1

        connector = "└── " if (is_last(i) or paths[i + 1].name in exclude) else "├── "

        print(f"{prefix}{connector}{path.name}")

        if path.is_dir():
            extension = "    " if is_last(i) else "│   "
            draw_tree(path, prefix + extension)


if __name__ == "__main__":
    root_path = pathlib.Path(".")
    print(f"{root_path.absolute().name}/")
    draw_tree(root_path)
