from flask import Flask, Response, render_template, send_file, jsonify
import cv2, os, os.path, time

app = Flask(__name__)
fifo = None

activemap = 0;

@app.route('/getpts', methods=['POST'])
def pts():
    global fifo
    if os.path.exists('fifo'):
        data = fifo.readline()
    else:
        fifo.close()
        return "Error: Server is dead";
    
    if not data == None and not data == "":
        cord = data.split(":")
        x = int(cord[0])
        y = int(cord[1])
        w = int(cord[2])
        s = int(cord[3])
        return jsonify(x=x, y=y, w=w, s=s, e=0)
    return jsonify(x=0, y=0, w=0, s=0, e=1)

@app.route('/getmaze', methods=['POST'])
def newmaze():
    maze = open("maze/maze{}.png".format(activemap%5), "rb")
    if maze.isOpen():
        return send_file(IO.BytesIO(maze.read()))
    else:
        maze.close()
        maze = open("maze/maze0.png")

@app.route('/')
def hi():
    return render_template("hello.html")

pid = os.fork();
if pid:
    time.sleep(1);
    if __name__ == "__main__":
        fifo = open('fifo', 'r')
        app.run();
else:
    os.system('python detectCircle.py')
