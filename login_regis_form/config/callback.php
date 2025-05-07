<?php
session_start();
require_once 'vendor/autoload.php';
require_once 'config.php';

use Hybridauth\Hybridauth;
use Hybridauth\HttpClient;

$provider = $_SESSION['provider'] ?? $_GET['provider'] ?? null;
if (!$provider) {
    die("No provider specified.");
}

$config = include 'oauth_config.php';

try {
    $hybridauth = new Hybridauth($config);
    $adapter = $hybridauth->authenticate($provider);
    $userProfile = $adapter->getUserProfile();

    // เอาข้อมูล user มาใช้
    $email = $userProfile->email;
    $name = $userProfile->displayName;

    // ตรวจสอบว่าเคยสมัครไว้แล้วหรือยัง
    $stmt = $pdo->prepare("SELECT * FROM users WHERE email = :email AND oauth_provider = :provider");
    $stmt->execute([
        'email' => $email,
        'provider' => $provider
    ]);
    $user = $stmt->fetch();

    if (!$user) {
        // ถ้ายังไม่เคยสมัคร -> สมัครใหม่อัตโนมัติ
        $identifier = $userProfile->identifier; // unique id จาก Google / Facebook
        $stmt = $pdo->prepare("INSERT INTO users (username, email, oauth_provider, oauth_id, created_at) VALUES (:username, :email, :oauth_provider, :oauth_id, NOW())");
        $stmt->execute([
            'username' => $name,
            'email' => $email,
            'oauth_provider' => $provider,
            'oauth_id' => $identifier
        ]);
        $userId = $pdo->lastInsertId();
    } else {
        $userId = $user['id'];
    }

    // Login สำเร็จ → สร้าง session
    $_SESSION['user_login'] = $userId;
    $_SESSION['username'] = $name;
    header("Location: ../index.php");
} catch (Exception $e) {
    echo "Oops! " . $e->getMessage();
}
