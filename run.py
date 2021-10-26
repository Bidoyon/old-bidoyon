from app import app

HOST = "localhost"
PORT = 5000

if __name__ == '__main__':
    app.run(HOST, PORT, debug=True)
