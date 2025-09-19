#!/usr/bin/env python3
"""
Syntax and bracket checking script for common web development file types.
Checks for unclosed brackets, braces, parentheses, and other common syntax errors.
"""

import os
import re
import json
import argparse
from typing import List, Dict, Tuple

class SyntaxChecker:
    def __init__(self):
        self.errors = []
        
    def check_brackets(self, content: str, filename: str) -> List[Dict]:
        """Check for unclosed brackets, braces, and parentheses."""
        errors = []
        stack = []
        line_num = 1
        
        # Mapping of opening to closing brackets
        pairs = {
            '(': ')',
            '[': ']',
            '{': '}',
        }
        
        for i, char in enumerate(content):
            if char == '\n':
                line_num += 1
                continue
                
            if char in pairs:
                stack.append((char, line_num, i))
            elif char in pairs.values():
                if not stack:
                    errors.append({
                        'file': filename,
                        'line': line_num,
                        'error': f'Unexpected closing bracket "{char}" without matching opening bracket',
                        'type': 'bracket_mismatch'
                    })
                else:
                    opening_char, opening_line, opening_pos = stack.pop()
                    expected_closing = pairs[opening_char]
                    if char != expected_closing:
                        errors.append({
                            'file': filename,
                            'line': line_num,
                            'error': f'Mismatched bracket: expected "{expected_closing}" but found "{char}" (opening bracket at line {opening_line})',
                            'type': 'bracket_mismatch'
                        })
        
        # Check for unclosed brackets
        for opening_char, opening_line, opening_pos in stack:
            errors.append({
                'file': filename,
                'line': opening_line,
                'error': f'Unclosed bracket "{opening_char}" - missing "{pairs[opening_char]}"',
                'type': 'unclosed_bracket'
            })
        
        return errors
    
    def check_php(self, content: str, filename: str) -> List[Dict]:
        """Check PHP-specific syntax issues."""
        errors = []
        
        # Check for PHP opening/closing tags
        if '<?php' in content and not content.strip().endswith('?>'):
            # This is actually correct - PHP files don't need closing tags
            pass
        
        # Check for missing semicolons (basic check)
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('//') and not line.startswith('/*'):
                # Check for statements that should end with semicolon
                if (re.match(r'^\s*(echo|print|return|\$\w+\s*=)', line) and 
                    not line.endswith(';') and not line.endswith('{') and
                    not line.endswith('}')):
                    errors.append({
                        'file': filename,
                        'line': i,
                        'error': 'Missing semicolon at end of statement',
                        'type': 'missing_semicolon'
                    })
        
        return errors
    
    def check_javascript(self, content: str, filename: str) -> List[Dict]:
        """Check JavaScript-specific syntax issues."""
        errors = []
        
        # Check for missing semicolons (basic check)
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('//') and not line.startswith('/*'):
                # Check for statements that should end with semicolon
                if (re.match(r'^\s*(let|const|var|\w+\s*=|return|console\.)', line) and 
                    not line.endswith(';') and not line.endswith('{') and
                    not line.endswith('}') and not line.endswith(',') and
                    not line.endswith(')')):
                    errors.append({
                        'file': filename,
                        'line': i,
                        'error': 'Missing semicolon at end of statement',
                        'type': 'missing_semicolon'
                    })
        
        return errors
    
    def check_css(self, content: str, filename: str) -> List[Dict]:
        """Check CSS-specific syntax issues."""
        errors = []
        
        # Remove comments first
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Check for missing closing braces for CSS rules
        lines = content.split('\n')
        in_rule = False
        rule_start_line = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('/*'):
                if '{' in line:
                    in_rule = True
                    rule_start_line = i
                elif '}' in line:
                    in_rule = False
                elif in_rule and line and not line.endswith(';') and ':' in line:
                    errors.append({
                        'file': filename,
                        'line': i,
                        'error': 'CSS property declaration should end with semicolon',
                        'type': 'missing_semicolon'
                    })
        
        return errors
    
    def check_html(self, content: str, filename: str) -> List[Dict]:
        """Check HTML-specific syntax issues."""
        errors = []
        
        # Check for unclosed HTML tags
        tag_stack = []
        self_closing_tags = {'img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 'source', 'track', 'wbr'}
        
        # Find all HTML tags
        tag_pattern = r'<(/?)(\w+)(?:\s[^>]*)?/?>'
        
        line_num = 1
        for match in re.finditer(tag_pattern, content):
            # Count lines up to this point
            line_num = content[:match.start()].count('\n') + 1
            
            is_closing = bool(match.group(1))
            tag_name = match.group(2).lower()
            is_self_closing = match.group(0).endswith('/>')
            
            if tag_name in self_closing_tags or is_self_closing:
                continue
            
            if is_closing:
                if not tag_stack:
                    errors.append({
                        'file': filename,
                        'line': line_num,
                        'error': f'Unexpected closing tag </{tag_name}> without matching opening tag',
                        'type': 'tag_mismatch'
                    })
                else:
                    opening_tag, opening_line = tag_stack.pop()
                    if opening_tag != tag_name:
                        errors.append({
                            'file': filename,
                            'line': line_num,
                            'error': f'Mismatched HTML tag: expected </{opening_tag}> but found </{tag_name}> (opening tag at line {opening_line})',
                            'type': 'tag_mismatch'
                        })
            else:
                tag_stack.append((tag_name, line_num))
        
        # Check for unclosed tags
        for tag_name, opening_line in tag_stack:
            errors.append({
                'file': filename,
                'line': opening_line,
                'error': f'Unclosed HTML tag <{tag_name}> - missing </{tag_name}>',
                'type': 'unclosed_tag'
            })
        
        return errors
    
    def check_json(self, content: str, filename: str) -> List[Dict]:
        """Check JSON syntax."""
        errors = []
        
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            errors.append({
                'file': filename,
                'line': e.lineno if hasattr(e, 'lineno') else 1,
                'error': f'JSON syntax error: {e.msg}',
                'type': 'json_syntax_error'
            })
        
        return errors
    
    def check_file(self, filepath: str) -> List[Dict]:
        """Check a single file for syntax errors."""
        if not os.path.exists(filepath):
            return [{
                'file': filepath,
                'line': 0,
                'error': 'File not found',
                'type': 'file_not_found'
            }]
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            return [{
                'file': filepath,
                'line': 0,
                'error': 'File encoding error - unable to read as UTF-8',
                'type': 'encoding_error'
            }]
        
        errors = []
        filename = os.path.basename(filepath)
        
        # Check brackets for all file types
        errors.extend(self.check_brackets(content, filename))
        
        # File-specific checks
        if filepath.endswith('.php'):
            errors.extend(self.check_php(content, filename))
        elif filepath.endswith('.js'):
            errors.extend(self.check_javascript(content, filename))
        elif filepath.endswith('.css'):
            errors.extend(self.check_css(content, filename))
        elif filepath.endswith('.html') or filepath.endswith('.htm'):
            errors.extend(self.check_html(content, filename))
        elif filepath.endswith('.json'):
            errors.extend(self.check_json(content, filename))
        
        return errors
    
    def check_directory(self, directory: str) -> List[Dict]:
        """Check all supported files in a directory."""
        all_errors = []
        supported_extensions = ['.php', '.js', '.css', '.html', '.htm', '.json']
        
        for root, dirs, files in os.walk(directory):
            # Skip .git and other hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if any(file.endswith(ext) for ext in supported_extensions):
                    filepath = os.path.join(root, file)
                    errors = self.check_file(filepath)
                    all_errors.extend(errors)
        
        return all_errors

def main():
    parser = argparse.ArgumentParser(description='Check code files for syntax errors and unclosed brackets')
    parser.add_argument('path', nargs='?', default='.', help='File or directory to check (default: current directory)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    checker = SyntaxChecker()
    
    if os.path.isfile(args.path):
        errors = checker.check_file(args.path)
    else:
        errors = checker.check_directory(args.path)
    
    if not errors:
        print("✅ No syntax errors found!")
        return 0
    
    # Group errors by file
    errors_by_file = {}
    for error in errors:
        filename = error['file']
        if filename not in errors_by_file:
            errors_by_file[filename] = []
        errors_by_file[filename].append(error)
    
    print(f"❌ Found {len(errors)} syntax error(s) in {len(errors_by_file)} file(s):\n")
    
    for filename, file_errors in errors_by_file.items():
        print(f"📄 {filename}:")
        for error in sorted(file_errors, key=lambda x: x['line']):
            line_info = f"Line {error['line']}: " if error['line'] > 0 else ""
            print(f"  ⚠️  {line_info}{error['error']}")
        print()
    
    return 1

if __name__ == '__main__':
    exit(main())