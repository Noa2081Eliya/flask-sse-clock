from flask import Flask, Response
import time

app = Flask(__name__)

# This function generates the current time and sends it to the client every second
def generate_time():
    while True:
        # Wait for 1 second before sending the next time update
        time.sleep(1)
        # Get the current time formatted as HH:MM:SS
        current_time = time.strftime("%H:%M:%S")
        # Yield the time in the required format for SSE: 'data: <message>\n\n'
        yield f"data: {current_time}\n\n"

# This route handles the SSE connection and streams the time to the client
@app.route('/time')
def time_stream():
    # Flask's Response object is used to send the data as an 'event-stream'
    return Response(generate_time(), mimetype='text/event-stream')

# This route serves a simple HTML page to display the time updates from the server
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SSE Time</title>
    </head>
    <body>
        <h1>Current Time:</h1>
        <div id="time"></div>

        <script>
            // Create a new EventSource object to listen for updates from the server
            const eventSource = new EventSource('/time');

            // When a message is received from the server, update the HTML content
            eventSource.onmessage = function(event) {
                document.getElementById('time').innerText = event.data;
            };
        </script>
    </body>
    </html>
    '''

# The main block to run the Flask application
if __name__ == '__main__':
    # Enable debug mode for development and allow threaded requests
    app.run(debug=True, threaded=True)
