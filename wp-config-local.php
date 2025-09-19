<?php
// Local development config
define('DB_NAME', 'wordpress');
define('DB_USER', 'root');  
define('DB_PASSWORD', '');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');

// Security keys - using dummy values for local development
define('AUTH_KEY',         'test-auth-key-123456789');
define('SECURE_AUTH_KEY',  'test-secure-auth-key-123456789');
define('LOGGED_IN_KEY',    'test-logged-in-key-123456789');
define('NONCE_KEY',        'test-nonce-key-123456789');
define('AUTH_SALT',        'test-auth-salt-123456789');
define('SECURE_AUTH_SALT', 'test-secure-auth-salt-123456789');
define('LOGGED_IN_SALT',   'test-logged-in-salt-123456789');
define('NONCE_SALT',       'test-nonce-salt-123456789');

define('WP_DEBUG', true);
