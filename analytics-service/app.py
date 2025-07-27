from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory store as fallback
stats_store = {}

@app.route('/increment', methods=['POST'])
def increment():
    data = request.get_json()
    key = data.get('key')
    if not key:
        return jsonify({'error': 'Missing key'}), 400
    stats_store[key] = stats_store.get(key, 0) + 1
    return jsonify({'message': f'{key} counter incremented'}), 200

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify(stats_store)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
