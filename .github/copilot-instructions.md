# WordPress on Pantheon Platform

This is a WordPress 6.8.2 installation configured to run on the [Pantheon hosting platform](https://pantheon.io). The repository is mirrored from Pantheon to GitHub via automated workflows.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Prerequisites & Setup
- Install WP-CLI for WordPress management:
  ```bash
  cd /tmp && wget https://github.com/wp-cli/wp-cli/releases/download/v2.10.0/wp-cli-2.10.0.phar
  chmod +x wp-cli-2.10.0.phar && sudo mv wp-cli-2.10.0.phar /usr/local/bin/wp
  ```
- PHP 8.3.6 is pre-installed with all necessary extensions (mysqli, curl, etc.)
- NEVER CANCEL: WP-CLI download takes 30-60 seconds. Set timeout to 120+ seconds.

### Quick Start Commands
- Check WordPress version: `wp core version`
- Verify WP-CLI setup: `wp --info`
- List available themes: `ls -la wp-content/themes/`
- List available plugins: `ls -la wp-content/plugins/`
- Start PHP development server: `php -S localhost:8080 -t .` (takes 2-3 seconds to start)

### Important Branch Information
- **master branch (731dde0c)**: Contains the full WordPress 6.8.2 codebase with all core files
- **main branch (a78bbf7)**: Contains minimal repository setup files only
- **Current working branch**: May be minimal - always checkout master branch hash to access WordPress files:
  ```bash
  git checkout 731dde0cf5022b96ae7cd5f45433e559610cbaa7
  ```

### Database Configuration
- **LOCAL DEVELOPMENT**: Database connections require proper MySQL setup which is complex in sandboxed environments
- **PANTHEON PRODUCTION**: Database config is handled automatically via `wp-config-pantheon.php`
- For local testing without database, many WP-CLI commands work: `wp core version`, `wp --info`
- Database-dependent operations (theme/plugin management, content) require environment-specific setup

### Configuration Files
- `wp-config.php`: Main configuration with conditional loading for different environments
- `wp-config-pantheon.php`: Pantheon-specific database and caching configuration  
- `wp-config-local.php`: Local development overrides (ignored by git)
- `pantheon.yml`: Platform configuration (PHP 8.2, MariaDB 10.4)
- `pantheon.upstream.yml`: Upstream WordPress defaults (DO NOT EDIT)

## Validation

### Always Validate These Commands Work
- `wp core version` - Should return "6.8.2"
- `php --version` - Should show PHP 8.3.6
- `ls wp-admin wp-content wp-includes` - Core WordPress directories must exist
- File structure check: `ls -1 | grep "wp-" | wc -1` should return 10+ files

### Manual Testing Steps
- ALWAYS checkout the master branch (731dde0c) before testing WordPress functionality
- Test WP-CLI basic commands that don't require database
- Verify WordPress core files are present and accessible
- DO NOT attempt full WordPress installation without proper database setup

### What Works vs. What Doesn't
✅ **WORKS**: 
- WP-CLI version/info commands
- PHP syntax validation of WordPress files
- File system operations (theme/plugin file inspection)
- Static file serving via PHP built-in server

❌ **REQUIRES SETUP**:
- Database-dependent WP-CLI commands (plugin install, theme activation)
- WordPress admin interface access
- Content management operations
- Full WordPress installation process

## Common Tasks

### Repository Navigation
```bash
# Get to WordPress codebase
git checkout 731dde0cf5022b96ae7cd5f45433e559610cbaa7

# Repository structure
ls -la
# Key directories: wp-admin/, wp-content/, wp-includes/
# Key files: wp-config.php, index.php, wp-login.php
```

### WordPress Core Information
- **Version**: 6.8.2 (verified via `wp core version`)
- **PHP Requirements**: 8.2+ (running on 8.3.6)
- **Database**: MariaDB 10.4 (Pantheon default)
- **Built-in Themes**: 15 themes available (twentyten through twentytwentyfive)
- **Built-in Plugins**: Akismet, Hello Dolly

### Development Workflow
- **GitHub Actions**: `.github/workflows/sync-pantheon.yml` handles Pantheon↔GitHub mirroring
- **Version Control**: Core WordPress files should not be modified directly
- **Customization**: Add themes/plugins to `wp-content/` directories
- **Configuration**: Use `wp-config-local.php` for local environment overrides

### Troubleshooting
- If WP-CLI says "This does not seem to be a WordPress installation", ensure you're on the master branch with WordPress files
- Database connection errors are expected without proper MySQL configuration
- 500 errors from PHP server indicate database connection issues, not WordPress core problems
- Network access may be limited - some WP-CLI commands requiring internet access may fail

## CRITICAL Reminders
- **NEVER CANCEL** long-running operations. Most commands complete within 30-60 seconds.
- **ALWAYS** checkout master branch (731dde0c) to access WordPress files
- **DO NOT** attempt database operations without proper environment setup
- **VERIFY** WordPress core files exist before running WP-CLI commands
- Use timeouts of 120+ seconds for any WP-CLI operations that might need internet access