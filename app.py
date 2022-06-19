import os

from flask import Flask, request, Response
from werkzeug.exceptions import BadRequest

from utils import build_query

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query/", methods=['POST'])
def perform_query() -> Response:
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    try:
        cmd_1 = request.args['cmd1']
        cmd_2 = request.args['cmd2']
        value_1 = request.args['value1']
        value_2 = request.args['value2']
        file_name = request.args['file_name']
    except:
        raise BadRequest(description=f'error in request parameters')

    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    path_file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_file):
        raise BadRequest(description=f'{file_name} was not found')

    with open(path_file) as file:
        res = build_query(file, cmd_1, value_1)
        res = build_query(res, cmd_2, value_2)
        content = '\n'.join(res)

    # вернуть пользователю сформированный результат
    return app.response_class(content, content_type="text/plain")


if __name__ == '__main__':
    app.run()
