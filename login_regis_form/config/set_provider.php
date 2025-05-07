<?php
session_start();
if (isset($_GET['provider'])) {
    $_SESSION['provider'] = $_GET['provider'];
    header("Location: callback.php");
    exit;
}
die("No provider set.");

?>