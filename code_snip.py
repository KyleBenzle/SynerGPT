from ANtalk import get_project_name
import re
import os

def save_code_to_file(code, filename):
    """Saves the given code string to a file in the 'code' directory, limiting the filename to 35 characters."""
    directory = "code"
    # Ensure the filename is limited to 35 characters
    filename = filename[:35]  # Removed the '.txt' extension
    if not os.path.exists(directory):
        os.makedirs(directory)
    full_path = os.path.join(directory, filename)
    with open(full_path, 'w') as file:
        file.write(code)
    print(f"Code saved to {full_path}")

def guess_language_from_code(code):
    """Guess the programming language from a code block using heuristic patterns."""
    patterns = {
        '.py': [r'\bdef\b', r'\bclass\b', r'import ', r'from .* import ', r'^\s*#'],
        '.js': [r'\bfunction\b', r'=\s*\(?\)?\s*=>', r'\bvar\b', r'\bconsole\.log\b', r'\bdocument\.getElementById\b'],
        '.html': [r'<!DOCTYPE html>', r'<html>', r'<head>', r'<body>', r'</html>'],
        '.css': [r'\{', r'\}', r':', r';', r'^\s*\.', r'^\s*#'],
        '.md': [r'^\s*#', r'^\s*###', r'\*\*', r'^\s*-', r'^\s*\*']
    }
    for extension, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
                return extension
    return '.txt'

def process_text_for_code_blocks(text):
    """Finds and saves code within the text to files, identifying explicit or guessing language."""
    # Pattern to find code blocks with optional language specifiers
    code_block_pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
    code_blocks = code_block_pattern.findall(text)
    for language, code in code_blocks:
        file_extension = guess_language_from_code(code) if not language else {
            'python': '.py',
            'html': '.html',
            'css': '.css',
            'javascript': '.js',
            'js': '.js',
            'markdown': '.md',
            'md': '.md'
        }.get(language.lower(), '.txt')
        project_name = get_project_name()
        filename = create_unique_filename(project_name, file_extension)
        save_code_to_file(code.strip(), filename)
        print(f"Saved code block to {filename}")
        return  # Stop after the first code block is found
    
    # Look for patterns in the whole text if no ``` delimited blocks are found
    file_extension = guess_language_from_code(text)
    if file_extension != '.txt':
        project_name = get_project_name()
        filename = create_unique_filename(project_name, file_extension)
        save_code_to_file(text.strip(), filename)
        print(f"Saved detected code to {filename}")

def create_unique_filename(base_name, extension):
    """Generates a unique filename to prevent overwrites."""
    filename = f"{base_name}{extension}"
    counter = 1
    while os.path.exists(os.path.join("code", filename)):
        filename = f"{base_name}_{counter}{extension}"
        counter += 1
    return filename