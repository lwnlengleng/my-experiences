<?php
session_start();

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
    }

    body {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
    }

    a {
        text-decoration: none;
        color: white;
        background: seagreen;
        border: 2px solid white;
        border-radius: 8px;
        padding: 15px 20px;
    }

    a:hover {
        background: white;
        color: seagreen;
        border: 2px solid seagreen;
    }

    .logout{
        background: brown;
    }
    .logout:hover{
        color: brown;
        border: 2px solid brown;
    }

</style>

<body>
    <h1>What's up guys !! Test Login form</h1>
    <?php if (isset($_SESSION['user_login'])) { ?>
        <a href="config/logout.php" class="logout">LOGOUT</a>
    <?php } else { ?>
        <a href="login-register.php" class="login">LOGIN</a>
    <?php } ?>

</body>

</html>