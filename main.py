from app import app
from flask import jsonify

# health check route
@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({"status": "server is up and running"})


# run the app
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
