<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vertical Navbar</title>
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

        body {
            min-height: 100vh;
            text-align: center;
        }

        .container {
            display: flex;
            flex-wrap: wrap;
            align-content: start;
            text-decoration: none;
        }

        .item:nth-child(1),
        .item:nth-child(4) {
            width: 100%;
            height: 5%;
        }

        .item:nth-child(2) {
            background: linear-gradient(15deg, rgb(218, 152, 152), rgb(177, 82, 82));
            width: 2%;
            height: 75%;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: .6s ease-in-out;
        }

        .item:nth-child(2) a{
            visibility: hidden;
        }

        .item:nth-child(2):hover{
            width: 25%;
            transition: .6s ease-in-out;
        }

        .item:nth-child(2):hover a {
            visibility: visible;
            background: slategray;
            color: white;
            font-weight: 500;
            text-align: center;
            text-decoration: none;
            border: 2px solid white;
            border-radius: 8px;
            box-shadow: 0 0 30px rgba(0, 0, 0, .2);
            margin: 10px 20px;
            padding: 10px 0;
            width: 80%;
        }

        .item:nth-child(2) a:hover {
            background: rgb(65, 124, 201);
            transition: .6s ease-in-out;
        }

        .item:nth-child(3) {
            display: flex;
            flex-wrap: wrap;
            flex-grow: 1;
            gap: 20px;
            margin: 2%;
        }

        .item:nth-child(3) .list {
            background: linear-gradient(15deg, rgb(219, 149, 149), rgb(255, 105, 105));
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, .2);
            flex: 1;
            transition: .6s ease-in-out;
        }

        .item:nth-child(3) .list:hover {
            flex-grow: 8;
            transition: .6s ease-in-out;
        }
    </style>
    <div class="container">
        <div class="item">**The side bar is located on the left side of the screen.**
            <i class='bx bxs-home'></i> Hover the cursur there.
        </div>
        <div class="item">
            <a href="#Home"><i class='bx bxs-home'></i> HOME</a>
            <a href="#News"><i class='bx bxs-news'></i> NEWS</a>
            <a href="#Contact"><i class='bx bxs-phone'></i> CONTACT</a>
            <a href="#About"><i class='bx bxs-building-house'></i> ABOUT</a>
        </div>
        <div class="item">
            <div class="list">NEWS 1</div>
            <div class="list">NEWS 2</div>
            <div class="list">NEWS 3</div>
            <div class="list">NEWS 4</div>
            <div class="list">NEWS 5</div>
            <div class="list">NEWS 6</div>
            <div class="list">NEWS 7</div>
            <div class="list">NEWS 8</div>
            <div class="list">NEWS 9</div>
        </div>
        <div class="item">Footer

        </div>
    </div>
</body>

</html>