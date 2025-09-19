# ky_wp

WordPress project with code syntax validation tools.

## Code Syntax Checker

This repository includes a Python-based syntax checker (`check_syntax.py`) that can identify common syntax errors in web development files, including:

### Supported File Types

- **PHP** (`.php`) - Checks for unclosed brackets, braces, parentheses, and missing semicolons
- **JavaScript** (`.js`) - Checks for bracket matching and basic syntax issues
- **CSS** (`.css`) - Checks for unclosed braces and missing semicolons in property declarations
- **HTML** (`.html`, `.htm`) - Checks for unclosed and mismatched HTML tags
- **JSON** (`.json`) - Validates JSON syntax

### Usage

```bash
# Check all files in current directory
python3 check_syntax.py

# Check specific file
python3 check_syntax.py example.php

# Check specific directory with verbose output
python3 check_syntax.py /path/to/directory --verbose
```

### Error Types Detected

1. **Unclosed Brackets** - Missing closing `}`, `)`, or `]`
2. **Mismatched Brackets** - Wrong type of closing bracket
3. **Missing Semicolons** - Missing `;` at end of statements
4. **Unclosed/Mismatched HTML Tags** - Missing or incorrect closing tags
5. **JSON Syntax Errors** - Invalid JSON format

### Example Files

The repository includes example files with common syntax errors for testing:

- `example.php` - PHP with bracket and semicolon issues (now fixed)
- `example.js` - JavaScript with unclosed braces (now fixed)
- `example.css` - CSS with unclosed selectors (now fixed)
- `example.html` - HTML with missing closing tags (now fixed)
- `example.json` - JSON with syntax errors (now fixed)

### Validation Results

After running the syntax checker and fixing all identified errors:

- ✅ PHP syntax: Valid (confirmed with `php -l`)
- ✅ JavaScript syntax: Valid (confirmed with `node -c`)
- ✅ JSON syntax: Valid (confirmed with Python JSON parser)
- ✅ CSS syntax: Valid (no unclosed selectors)
- ✅ HTML structure: Valid (properly nested tags)

## Development

The syntax checker is designed to catch the most common coding errors that can break websites and applications. It focuses on structural issues like bracket matching rather than style or best practice violations.