import os

FOLDER = "icons"
PATH = "icons/"
COLOR_SUFFIX = "-2af1f1"
EXT = ".svg"
README = "README.md"

folder = os.path.join(os.getcwd(), FOLDER)

icons = []

# 1. Renombrar archivos dentro de la carpeta de iconos
for file in os.listdir(folder):
    if not file.lower().endswith(EXT):
        continue

    name = file[:-4]

    if name.endswith(COLOR_SUFFIX):
        # Ya tiene el sufijo de color esperado
        icons.append(file)
        continue

    new_name = f"{name}{COLOR_SUFFIX}{EXT}"
    os.rename(
        os.path.join(folder, file),
        os.path.join(folder, new_name)
    )
    icons.append(new_name)

# Nos aseguramos de tener la lista ordenada
icons = sorted(set(icons))

# 2. Actualizar la sección de Icons en el README.md
readme_path = os.path.join(os.getcwd(), README)

with open(readme_path, "r", encoding="utf-8") as f:
    readme_lines = f.readlines()

# Buscamos el bloque que empieza en el div de iconos
start_idx = None
end_idx = None

for i, line in enumerate(readme_lines):
    if line.startswith('<div style="display:inline;">'):
        start_idx = i
    if line.strip() == "</details>":
        end_idx = i

if start_idx is None or end_idx is None or end_idx <= start_idx:
    raise RuntimeError("No se pudo encontrar el bloque de Icons en README.md")

new_block = []

# Bloque HTML de iconos (tamaños actualizados aquí)
new_block.append('<div style="display:inline;">\n')
for icon in icons:
    new_block.append(
        f'  <img src="{PATH}{icon}" style="width:24px;height:24px;" />\n'
    )
new_block.append('<div/>\n')
new_block.append("\n")

# Bloque con listado de nombres
new_block.append("<details>\n")
new_block.append("  <summary>Listado de nombres</summary>\n")
new_block.append("  \n")
new_block.append("  ```md\n")
for icon in icons:
    new_block.append(f"  {icon}\n")
new_block.append("  ```\n")
new_block.append("</details>\n")

# Reemplazamos el bloque antiguo por el nuevo
updated_readme_lines = (
    readme_lines[:start_idx] + new_block + readme_lines[end_idx + 1 :]
)

with open(readme_path, "w", encoding="utf-8") as f:
    f.writelines(updated_readme_lines)

print("Renombrado de iconos y actualización de README.md completa.")
