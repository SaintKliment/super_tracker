from flask import Flask, request, jsonify

app = Flask(__name__)

# Локальная переменная для хранения зарегистрированных узлов
nodes = []

# Маршрут для регистрации узла
@app.route('/register', methods=['POST'])  # {"ip": "192.168.1.100", "port": 12345, "id": "node-123"} - тело для регистрации
def register_node():
    # Получаем данные из тела запроса (JSON)
    data = request.json
    ip = data.get('ip')
    port = data.get('port')
    node_id = data.get('id')

    # Проверяем, что IP, порт и ID переданы
    if not ip or not port or not node_id:
        return jsonify({"error": "IP, port, and ID are required"}), 400

    # Проверяем, не зарегистрирован ли уже узел с таким же IP, портом или ID
    for node in nodes:
        if node['ip'] == ip and node['port'] == port:
            return jsonify({"error": "Node with the same IP and port already registered"}), 409  # 409 Conflict
        if node['id'] == node_id:
            return jsonify({"error": "Node with the same ID already registered"}), 409  # 409 Conflict

    # Создаем запись об узле
    node = {
        "ip": ip,
        "port": port,
        "id": node_id
    }

    # Добавляем узел в список
    nodes.append(node)

    # Возвращаем успешный ответ
    return jsonify({"message": "Node registered successfully", "node": node}), 200

@app.route('/nodes', methods=['GET'])
def get_nodes():
    # Получаем IP, порт и ID запрашивающего узла из параметров запроса
    requester_ip = request.args.get('ip')
    requester_port = request.args.get('port')
    requester_id = request.args.get('id')

    # Если IP, порт или ID не переданы, возвращаем все узлы
    if not requester_ip or not requester_port or not requester_id:
        return jsonify({"nodes": nodes}), 200

    # Преобразуем порт в целое число
    try:
        requester_port = int(requester_port)
    except ValueError:
        return jsonify({"error": "Invalid port value"}), 400

    # Фильтруем список узлов, исключая запрашивающий узел
    filtered_nodes = [
        node for node in nodes
        if not (node['ip'] == requester_ip and node['port'] == requester_port and node['id'] == requester_id)
    ]

    # Возвращаем отфильтрованный список узлов
    return jsonify({"nodes": filtered_nodes}), 200
    
# Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)