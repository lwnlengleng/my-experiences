<?php
return [
    'callback' => 'http://localhost/login_regis_form/config/callback.php',
    'providers' => [
        'Google' => [
            'enabled' => true,
            'keys' => ['id' => 'GOOGLE_CLIENT_ID', 'secret' => 'GOOGLE_CLIENT_SECRET'],
            'scope' => 'email profile',
        ],
        'GitHub' => [
            'enabled' => true,
            'keys' => ['id' => 'GITHUB_CLIENT_ID', 'secret' => 'GITHUB_CLIENT_SECRET'],
            'scope' => 'user:email',
        ],
        'Facebook' => [
            'enabled' => true,
            'keys' => ['id' => 'FACEBOOK_APP_ID', 'secret' => 'FACEBOOK_APP_SECRET'],
            'scope' => 'email',
        ],
        'LinkedIn' => [
            'enabled' => true,
            'keys' => ['id' => 'LINKEDIN_CLIENT_ID', 'secret' => 'LINKEDIN_CLIENT_SECRET'],
            'scope' => 'r_liteprofile r_emailaddress',
        ],
    ],
];
