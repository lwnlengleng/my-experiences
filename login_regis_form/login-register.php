<?php
session_start();

// บล็อคไม่ให้เข้าหน้า login ถ้า User ล็อกอินอยู่
if (isset($_SESSION['user_login'])) {
    header("Location: index.php"); // รีเฟรชหน้า login ใหม่หลัง logout
    exit();
}
?>


<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="style/login-register.css?v=<?php echo time(); ?>">

</head>

<body>
    <div class="container">
        <div class="form-box login">
            <form action="config/auth.php" method="POST">
                <a class="home-btn" href="index.php"><i class='bx bxs-home'></i></a>
                <h1>LOGIN</h1>

                <?php if (isset($_SESSION['error'])) { ?>
                    <div class="alert alert-danger" style="color: brown">
                        <?php
                        echo $_SESSION['error'];
                        unset($_SESSION['error']);
                        ?>
                    </div>
                <?php } ?>

                <?php if (isset($_SESSION['success'])) { ?>
                    <div class="alert alert-success" style="color: seagreen">
                        <?php
                        echo $_SESSION['success'];
                        unset($_SESSION['success']);
                        ?>
                    </div>
                <?php } ?>

                <div class="input-box">
                    <input type="text" name="username" placeholder="Username" required>
                    <i class='bx bxs-user-pin'></i>
                </div>
                <div class="input-box">
                    <input type="password" name="password" placeholder="Password" required>
                    <i class='bx bxs-lock-alt'></i>
                </div>
                <div class="forgot-link">
                    <a href="#">forgot password?</a>
                </div>
                <button type="submit" name="login" class="btn">Login</button>
                <p> or login with socials platform</p>
                <div class="social-icons">
                    <a href="config/set_provider.php?provider=Google"><i class='bx bxl-google-plus'></i></a>
                    <a href="config/callback.php?provider=Facebook"><i class='bx bxl-facebook-circle'></i></a>
                    <a href="config/callback.php?provider=GitHub"><i class='bx bxl-github'></i></a>
                    <a href="config/callback.php?provider=LinkedIn"><i class='bx bxl-linkedin-square'></i></a>
                </div>
            </form>
        </div>

        <div class="form-box register">
            <form action="config/auth.php" method="POST">
                <a class="home-btn" href="index.php"><i class='bx bxs-home'></i></a>
                <h1>REGISTRATION</h1>

                <?php if (isset($_SESSION['error'])) { ?>
                    <div class="alert alert-danger" style="color: brown">
                        <?php
                        echo $_SESSION['error'];
                        unset($_SESSION['error']);
                        ?>
                    </div>
                <?php } ?>

                <?php if (isset($_SESSION['success'])) { ?>
                    <div class="alert alert-success" style="color: seagreen">
                        <?php
                        echo $_SESSION['success'];
                        unset($_SESSION['success']);
                        ?>
                    </div>
                <?php } ?>

                <div class="input-box">
                    <input type="text" name="username" placeholder="Username" required>
                    <i class='bx bxs-user-pin'></i>
                </div>
                <div class="input-box">
                    <input type="password" name="password" placeholder="Password" required>
                    <i class='bx bxs-lock-alt'></i>
                </div>
                <div class="input-box">
                    <input type="email" name="email" placeholder="Email" required>
                    <i class='bx bxs-envelope'></i>
                </div>
                <div class="input-box">
                    <input type="text" name="phone_number" placeholder="Phone Number" required>
                    <i class='bx bxs-phone'></i>
                </div>

                <button type="submit" name="register" class="btn">Register</button>
            </form>
        </div>

        <div class="toggle-box">
            <div class="toggle-panel toggle-left">
                <h1>Hello, Welcome!</h1>
                <p>Don't have an account?</p>
                <button class="btn register-btn">Register</button>
            </div>
            <div class="toggle-panel toggle-right">
                <h1>Welcome Back!</h1>
                <p>Already have an account?</p>
                <button class="btn login-btn">Login</button>
            </div>
        </div>

    </div>

    <script src="script/script.js"></script>
</body>

</html>