<?php
session_start();
require 'config.php';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // REGISTER
    if (isset($_POST["register"])) {
        $username = strtolower(trim($_POST["username"]));
        $phone_number = trim($_POST["phone_number"]);
        $email = trim($_POST["email"]);
        $password = trim($_POST["password"]);

        if (empty($username) || empty($phone_number) || empty($email) || empty($password)) {
            $_SESSION['error'] = "กรุณากรอกข้อมูลให้ครบถ้วน";
            header("Location: ../login-register.php");
            exit;
        }

        // ตรวจสอบ email ซ้ำ
        $stmt = $pdo->prepare("SELECT id FROM users WHERE email = :email");
        $stmt->execute(['email' => $email]);
        if ($stmt->fetch()) {
            $_SESSION['error'] = "อีเมลนี้ถูกใช้แล้ว";
            header("Location: ../login-register.php");
            exit;
        }

        // ตรวจสอบ username ซ้ำ
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM users WHERE LOWER(username) = :username");
        $stmt->execute(['username' => $username]);
        $exists = $stmt->fetchColumn();

        if ($exists > 0) {
            $_SESSION['error'] = "ชื่อผู้ใช้นี้ถูกใช้แล้ว";
            header("Location: ../login-register.php");
            exit;
        }

        // แฮชรหัสผ่าน และเพิ่มข้อมูลลง DB
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        $sql = "INSERT INTO users (username, phone_number, email, password) 
                VALUES (:username, :phone_number, :email, :password)";
        $stmt = $pdo->prepare($sql);
        if (
            $stmt->execute([
                'username' => $username,
                'phone_number' => $phone_number,
                'email' => $email,
                'password' => $hashed_password
            ])
        ) {
            $_SESSION['success'] = "สมัครสมาชิกสำเร็จ!";
        } else {
            $_SESSION['error'] = "เกิดข้อผิดพลาด กรุณาลองใหม่";
        }

        header("Location: ../login-register.php");
        exit;
    }

    // LOGIN
    if (isset($_POST["login"])) {
        $username = strtolower(trim($_POST["username"]));
        $password = trim($_POST["password"]);

        $stmt = $pdo->prepare("SELECT * FROM users WHERE LOWER(username) = :username");
        $stmt->execute(['username' => $username]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['user_login'] = $user['id'];
            $_SESSION['success'] = "เข้าสู่ระบบสำเร็จ!";
            header("Location: ../index.php");
            exit;
        } else {
            $_SESSION['error'] = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง';
            header("Location: ../login-register.php");
            exit;
        }
    }

} catch (PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}
?>