<?php

    $host = "localhost"; // Database host
    $dbname = "login_register"; // Database name
    $username = "root"; // Database username
    $password = "root"; // Database password

    try {
        // Create a new PDO instance
        $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);

        // Set PDO to throw exceptions on errors
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // echo "Connected successfully!";
    } catch (PDOException $e) {
        die("Connection failed: " . $e->getMessage());
    }

?>