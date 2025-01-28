from flask import Flask, request, jsonify

app = Flask(__name__)

# Локальная переменная для хранения зарегистрированных узлов
nodes = []

# Маршрут для регистрации узла
@app.route('/register', methods=['POST'])  # {"ip": "192.168.1.100", "port": 12345} - тело для регистрации
def register_node():
    # Получаем данные из тела запроса (JSON)
    data = request.json
    ip = data.get('ip')
    port = data.get('port')

    # Проверяем, что IP и порт переданы
    if not ip or not port:
        return jsonify({"error": "IP and port are required"}), 400

    # Проверяем, не зарегистрирован ли уже узел с таким же IP и портом
    for node in nodes:
        if node['ip'] == ip and node['port'] == port:
            return jsonify({"error": "Node already registered"}), 409  # 409 Conflict

    # Создаем запись об узле
    node = {
        "ip": ip,
        "port": port
    }

    # Добавляем узел в список
    nodes.append(node)

    # Возвращаем успешный ответ
    return jsonify({"message": "Node registered successfully", "node": node}), 200

# Маршрут для получения списка зарегистрированных узлов
@app.route('/nodes', methods=['GET'])
def get_nodes():
    # Получаем IP и порт запрашивающего узла из параметров запроса
    requester_ip = request.args.get('ip')
    requester_port = request.args.get('port')

    # Если IP и порт не переданы, возвращаем все узлы
    if not requester_ip or not requester_port:
        return jsonify({"nodes": nodes}), 200

    # Фильтруем список узлов, исключая запрашивающий узел
    filtered_nodes = [
        node for node in nodes
        if not (node['ip'] == requester_ip and node['port'] == int(requester_port))
    ]

    # Возвращаем отфильтрованный список узлов
    return jsonify({"nodes": filtered_nodes}), 200

# Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)