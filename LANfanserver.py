from flask import Flask, request, render_template, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '555'
socketio = SocketIO(app)

# Valid fan speeds
valid_speeds = ["0", "4", "2", "1"]

# Global variable to store the last fan speed
last_fan_speed = "0"  # Default to 0

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def handle_request():
    global last_fan_speed  # Access the global variable
    if request.method == 'OPTIONS':
        # Handle preflight requests
        response = app.response_class(
            response="",
            status=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        )
        return response
    elif request.method == 'GET':
        # Render the HTML template
        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Cooling Fan Control</title>
   <style>
       * {
           margin: 0;
           padding: 0;
           box-sizing: border-box;
       }

       body {
           font-family: "Poppins", sans-serif;
           background: #cfd0d0;
           color: #333333;
           display: flex;
           align-items: center;
           justify-content: center;
           height: 100vh;
           flex-direction: column;
       }

       .container {
           width: 100%;
           display: flex;
           align-items: center;
           justify-content: space-around;
           flex-direction: column;
       }

       .svg {
           width: 90%;
           margin: 0 auto;
           overflow: hidden;
           display: flex;
           align-items: center;
           justify-content: center;
       }

       .svg img {
           width: 400px;
       }

       .buttons {
           display: flex;
           align-items: center;
           justify-content: space-between;
           width: 300px;
       }

       .buttons p {
           background: #cfd0d0;
           box-shadow: 5px 5px 13px #b6b7b7, -5px -5px 13px #e8e9e9;
           padding: 10px 20px;
           cursor: pointer;
           user-select: none;
           border-radius: 5px;
           font-weight: 900;
       }

       .buttons p:active {
           box-shadow: inset 5px 5px 13px #b6b7b7, inset -5px -5px 13px #e8e9e9;
       }

       .one, .two, .third, .stop {
           animation: rotate linear infinite;
           animation-play-state: running;
       }

       @keyframes rotate {100% {transform: rotate(360deg);}}

       @media only screen and (max-width: 400px) {
           .svg img {
               min-width: 320px;
           }
       }

html{
    overflow: hidden;
}

body{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
}

.fan{
    width: 500px;
    height: 500px;
    position: relative;
    z-index: 1;
}
.fan-main{
    position: absolute;
    width: 200px;
    bottom: 50px;
    left: 50%;
    transform: translateX(-50%);
}



.fan .head .green{
    position: absolute;
    width: 30px;
    height: 20px;
    border-radius: 5px;
    left: 30%;
    background: #32ba7c;
    cursor: pointer;
    z-index: 1;
    bottom: -35%;
}

.fan .head{
    transition: 1s transform;
    height: 300px;
    width: 300px;
    position: absolute;
    bottom: 195px;
    left: calc(50% - 150px);
}

.fan .head .engine{
    position: absolute;
    top: 100px;
    width: 100px;
    height: 100px;
    background: #2f423f;
    border-radius: 50%;
    left: 49%;
    transform: translateX(-50%);
}


.fan-blades{
    width: 220px;
    height: 220px;
    position: absolute;
    transition: 4s;
    top: 13%;
    left: calc(50% - 115px);
    transform-origin: center center;
    z-index: 1;
    animation: start infinite 1s linear forwards;
}

.fan-blades .blade {
    position: absolute;
    width: 40px;
    height: 100%;
    left: 50%;
    transform: translateX(-50%);
    perspective: 500px;
    transform-style: preserve-3d;
}

.fan-blades .blade:nth-child(2){
    transform: translateX(-50%) rotate(90deg);
}
.fan-blades .blade:nth-child(3){
    transform: translateX(-50%) rotate(180deg);
}
.fan-blades .blade:nth-child(4){
    transform: translateX(-50%) rotate(270deg);
}

.fan-blades .blade span{
    width: 100%;
    height: 200%;
    border-radius: 44px;
    background: #222;
    position: absolute;
    top: -66px;
    display: block;
    transform-style: preserve-3d;
    transform: rotateX(78deg);
    overflow: hidden;
}

.fan-blades .blade span::after{
    width: 50%;
    height: 100%;
    content: "";
    display: block;
    background: #333;
    transform: rotateX(0deg);
}

.fan-blades .center{
    position: absolute;
    overflow: hidden;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%) rotate(45deg);
    background: #ccc;
    z-index: 2;
}
.fan-blades .center::after{
    content: "";
    width: 40px;
    height: 20px;
    background: #888;
    display: block;
}


#start:checked + div > .fan-blades {
    animation: off 0.5s ease-out forwards;
}
#start:checked + div > .green{
    bottom: -36%;
}
#start:checked + div > .green:before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 4px;
    width: 100%;
    background: #666;
}

@keyframes start{
    from{
        transform: rotate(0deg);
    }
    to{
        transform: rotate(360deg);
    }
}
@keyframes off{
    to{
        transform: rotate(360deg);
    }
}

   </style>
</head>
<body>
   <div class="container">
       <h1>Fan</h1>
       <div class="fan">
    <div class="fan-main">
        <div class="bottom"></div>
    </div>
    <div class="fan-blades">
        <span class="center"></span>
        <div class="blade"><span></span></div>
        <div class="blade"><span></span></div>
        <div class="blade"><span></span></div>
        <div class="blade"><span></span></div>
    </div>
</div>

       <div class="buttons">
           <p class="stop">OFF</p>
           <p class="first">LOW</p>
           <p class="second">MED</p>
           <p class="third">HIGH</p>
       </div>
   </div>

   <!-- Your existing HTML code ... -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.4/socket.io.js"></script>
<script>
    const socket = io();

    socket.on('fan_speed_update', (data) => {
        const fanBlades = document.querySelector(".fan-blades");
        const lastFanSpeed = data.fanSpeed;

        // Update the fan animation based on the received fan speed
        const rotationSpeed = lastFanSpeed === "0" ? 0 : parseInt(lastFanSpeed);
        fanBlades.style.animationDuration = `${rotationSpeed}s`;
    });
    document.addEventListener("DOMContentLoaded", function () {
        const fanBlades = document.querySelector(".fan-blades");

        // Initialize the fan animation based on the last fan speed
        const initialSpeed = "{{ last_fan_speed }}" === "0" ? 0 :        	parseInt("{{ last_fan_speed }}");
        fanBlades.style.animationDuration = `${initialSpeed}s`;

        document.querySelectorAll(".buttons p").forEach((btn) => {
            btn.addEventListener("click", (e) => {
                let rotationSpeed;

                if (e.target.classList.contains("first")) {
                    rotationSpeed = 4; // Low speed
                } else if (e.target.classList.contains("second")) {
                    rotationSpeed = 2; // Mid speed
                } else if (e.target.classList.contains("third")) {
                    rotationSpeed = 1; // High speed
                } else if (e.target.classList.contains("stop")) {
                    rotationSpeed = 0; // Stop
                }

                // Update the rotation style based on the selected speed
                fanBlades.style.animationDuration = `${rotationSpeed}s`;

                // Send the selected fan speed to the server
                fetch("/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: `fanSpeed=${rotationSpeed}`,
                })
                    .then((response) => response.text())
                    .then((data) => console.log(data))
                    .catch((error) => console.error(error));
            });
        });
    });
</script>

<!-- Your existing HTML code ... -->

</body>
</html>""",last_fan_speed=last_fan_speed)
   
    elif request.method == 'POST':
        # Extract the fan speed from the request form
        fan_speed = request.form.get('fanSpeed')

        # Check if the received command is a valid fan speed
        if fan_speed in valid_speeds:
            print(f"Received valid fan speed command: {fan_speed}")

            #Update the last fan speed variable
            #global last_fan_speed
            last_fan_speed = fan_speed

        # Emit the fan speed update event to all connected clients
        socketio.emit('fan_speed_update', {'fanSpeed': fan_speed})
        return "Fan speed changed"
    else:
        print(f"Received invalid fan speed command: {fan_speed}")
        return "Invalid fan speed"

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=12345)
