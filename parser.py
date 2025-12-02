import configparser

def get_config(filename: str, section: str, key: str):
    with open(filename) as f:
        content = f.read()

    # Prepend a dummy section if the file starts with key-value lines
    content = "[DUMMY]\n" + content
    config = configparser.ConfigParser()
    config.optionxform = str
    from io import StringIO
    config.read_file(StringIO(content))
    value = config.get(section, key)

    return value

def set_config(filename: str, section: str, key: str, value: str):
    with open(filename) as f:
        lines = f.readlines()

    current_section = None
    updated = False
    new_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('[') and stripped.endswith(']'):
            current_section = stripped[1:-1]
            new_lines.append(line)
            continue

        if '=' in line and current_section == section and not updated:
            k, v = line.split('=', 1)
            k = k.strip()
            if k == key:
                new_lines.append(f"  {k} = {value}\n")
                updated = True
                continue

        new_lines.append(line)

    # If key not found, append at the end of the first occurrence of section
    if not updated:
        for i, line in enumerate(new_lines):
            if line.strip() == f"[{section}]":
                new_lines.insert(i+1, f"  {key} = {value}\n")
                break

    with open(filename, 'w') as f:
        f.writelines(new_lines)
    