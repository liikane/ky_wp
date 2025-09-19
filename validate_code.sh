#!/bin/bash

# Code validation script using standard tools
# This script checks code files for syntax errors using built-in language validators

echo "🔍 Code Syntax Validation Report"
echo "================================"
echo

ERROR_COUNT=0

# Check PHP files
echo "🐘 Checking PHP files..."
for file in *.php; do
    if [ -f "$file" ]; then
        echo -n "  Checking $file... "
        if php -l "$file" > /dev/null 2>&1; then
            echo "✅ Valid"
        else
            echo "❌ Syntax Error"
            php -l "$file" 2>&1 | sed 's/^/    /'
            ((ERROR_COUNT++))
        fi
    fi
done

# Check JavaScript files
echo
echo "🟡 Checking JavaScript files..."
for file in *.js; do
    if [ -f "$file" ]; then
        echo -n "  Checking $file... "
        if node -c "$file" > /dev/null 2>&1; then
            echo "✅ Valid"
        else
            echo "❌ Syntax Error"
            node -c "$file" 2>&1 | sed 's/^/    /'
            ((ERROR_COUNT++))
        fi
    fi
done

# Check JSON files
echo
echo "📄 Checking JSON files..."
for file in *.json; do
    if [ -f "$file" ]; then
        echo -n "  Checking $file... "
        if python3 -c "import json; json.loads(open('$file').read())" > /dev/null 2>&1; then
            echo "✅ Valid"
        else
            echo "❌ Syntax Error"
            python3 -c "import json; json.loads(open('$file').read())" 2>&1 | sed 's/^/    /'
            ((ERROR_COUNT++))
        fi
    fi
done

# Check CSS files (basic bracket matching)
echo
echo "🎨 Checking CSS files..."
for file in *.css; do
    if [ -f "$file" ]; then
        echo -n "  Checking $file... "
        # Count opening and closing braces
        OPEN=$(grep -o '{' "$file" | wc -l)
        CLOSE=$(grep -o '}' "$file" | wc -l)
        if [ "$OPEN" -eq "$CLOSE" ]; then
            echo "✅ Brackets balanced ($OPEN pairs)"
        else
            echo "❌ Bracket mismatch (${OPEN} opening, ${CLOSE} closing)"
            ((ERROR_COUNT++))
        fi
    fi
done

# Check HTML files (basic tag structure)
echo
echo "🌐 Checking HTML files..."
for file in *.html *.htm; do
    if [ -f "$file" ]; then
        echo -n "  Checking $file... "
        # Use Python to validate basic HTML structure
        if python3 -c "
import re
with open('$file', 'r') as f:
    content = f.read()

# Basic HTML validation - check for properly closed tags
tags = []
for match in re.finditer(r'<(/?)(\w+)(?:\s[^>]*)?/?>', content):
    is_closing = bool(match.group(1))
    tag_name = match.group(2).lower()
    is_self_closing = match.group(0).endswith('/>')
    
    # Skip self-closing tags and common void elements
    void_elements = {'img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 'source', 'track', 'wbr'}
    if tag_name in void_elements or is_self_closing:
        continue
    
    if is_closing:
        if not tags or tags[-1] != tag_name:
            raise Exception(f'Mismatched tag: {tag_name}')
        tags.pop()
    else:
        tags.append(tag_name)

if tags:
    raise Exception(f'Unclosed tags: {tags}')
" > /dev/null 2>&1; then
            echo "✅ Valid"
        else
            echo "❌ Structure Error"
            python3 -c "
import re
with open('$file', 'r') as f:
    content = f.read()

tags = []
for match in re.finditer(r'<(/?)(\w+)(?:\s[^>]*)?/?>', content):
    is_closing = bool(match.group(1))
    tag_name = match.group(2).lower()
    is_self_closing = match.group(0).endswith('/>')
    
    void_elements = {'img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 'source', 'track', 'wbr'}
    if tag_name in void_elements or is_self_closing:
        continue
    
    if is_closing:
        if not tags or tags[-1] != tag_name:
            print(f'    Mismatched tag: expected </{tags[-1] if tags else \"??\"}> but found </{tag_name}>')
            break
        tags.pop()
    else:
        tags.append(tag_name)

if tags:
    print(f'    Unclosed tags: {tags}')
" 2>/dev/null
            ((ERROR_COUNT++))
        fi
    fi
done

echo
echo "================================"
if [ $ERROR_COUNT -eq 0 ]; then
    echo "🎉 All files passed validation!"
    exit 0
else
    echo "❌ Found $ERROR_COUNT file(s) with syntax errors"
    exit 1
fi