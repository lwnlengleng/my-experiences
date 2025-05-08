<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
$cart = isset($_SESSION['cart']) ? $_SESSION['cart'] : [];
$cartCount = array_sum(array_column($cart, 'quantity'));
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navbar</title>
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
</head>

<body>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        .hidden {
            display: none;
        }

        .nav-container {
            position: sticky;
            align-items: center;
            justify-content: center;
            top: 0;
            width: 100%;
            z-index: 1000;
        }

        .nav-bar {
            position: sticky;
            display: flex;
            align-content: center;
            justify-content: center;
            top: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(120deg, rgb(124, 78, 150), rgb(191, 145, 218));
            background-size: cover;
            background-position: center;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 0 30px rgba(0, 0, 0, .2);
            font-weight: 600;
            padding: 5px 10%;
            transition: .6s ease-in-out;
            z-index: 1000;
        }

        .nav-bar a {
            text-align: center;
            color: #eee;
            background: rgb(71, 70, 70);
            border-radius: 10px;
            border: 2px solid #eee;
            margin: 10px 20px 10px 20px;
            padding: 10px 20px;
            text-decoration: none;
        }

        .nav-bar .btn.btn-outline-light.me-2 {
            position: absolute;
            display: flex;
            justify-content: center;
            align-items: center;
            right: 0;
            width: 10%;
            max-width: 100px;
            background: seagreen;
        }

        .nav-bar .btn.btn-outline-light.me-2:hover {
            background: transparent;
        }

        .nav-bar .btn.btn-danger {
            position: absolute;
            right: 0;
            background: rgb(209, 112, 112);
        }

        .nav-bar .btn.btn-danger:hover {
            background: transparent;
        }

        .nav-bar a:hover {
            color: #fff;
            background: transparent;
            transition: .6s ease-in-out;
        }

        .cart-icon {
            position: relative;
        }

        #cart-count {
            position: absolute;
            top: -10px;
            right: -10px;
            background: rgb(231, 63, 63);
            color: white;
            font-size: 12px;
            padding: 2px 6px;
            border-radius: 50%;
        }

        @media screen and (max-width: 940px) {
            .nav-bar a {
                font-size: 10px;
                text-align: center;
                margin: 10px;
                padding: 10px 20px;
                height: auto;
                transition: .6s ease-in-out;
            }
        }

        @media screen and (max-width: 576px) {
            .nav-bar a {
                font-size: 10px;
                padding: 4px 8px;
                margin: 4px;
                height: auto;
                transition: .6s ease-in-out;
            }

            .nav-bar .btn.btn-danger {
                top: 100%;
            }
        }
    </style>

    <div class="nav-container">
        <nav class="nav-bar">
            <a href="#home">HOME
                <i class='bx bxs-home'></i>
            </a>
            <a href="#menu">MENU
                <i class='bx bxs-bowl-rice'></i>
            </a>
            <a href="#contact">CONTACT
                <i class='bx bxs-phone'></i>
            </a>
            <?php if (!isset($_SESSION['user_login'])): ?>
                <a href="#driver-login">DRIVER<i class='bx bxs-truck'></i></a>
            <?php endif; ?>


            <?php
            if (isset($_SESSION['user_login'])) { ?>
                <a href="#logout" class="btn btn-danger">LOGOUT</a>
                <a href="#cart" class="cart-icon">
                    <i class='bx bx-cart'></i>
                    <span id="cart-count"><?= $cartCount ?></span>
                </a>
                <a href="#user-orders">MY ORDERS</a>

            <?php } elseif (isset($_SESSION['driver_login'])) { ?>
                <a class="hidden">LOGIN</a>
            <?php } else { ?>
                <a href="#login-page" class="btn btn-outline-light me-2">LOGIN</a>
            <?php } ?>

            <?php if (isset($_SESSION['driver_login'])) { ?>
                <a href="#driver-logout-page" class="btn btn-danger">DRIVER LOGOUT</a>
            <?php } else { ?>
                <a class="hidden">LOGIN</a>
            <?php } ?>

        </nav>
    </div>
</body>

</html>