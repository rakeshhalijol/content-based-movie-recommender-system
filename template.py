import os

# Define folder structure
folders = [
    "./notebooks",
    "./Datasets",
    "./Models",
    "./src"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create placeholder files
with open("./notebooks/experiments.ipynb", "w") as f:
    f.write('{}')  # Empty JSON content (valid .ipynb file)

with open("./src/main.py", "w") as f:
    f.write("# Streamlit entry point\n\nif __name__ == '__main__':\n    pass\n")

print("Project structure created successfully.")
