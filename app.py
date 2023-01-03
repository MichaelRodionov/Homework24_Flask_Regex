from typing import Optional

from flask import Flask, abort, request, Response
import os

from utils.constants import DATA_DIR
from classes.user_request import UserRequest
from utils.exceptions import EmptyArgs, SortValue, MapValue, LimitValue, WrongArgs

# ----------------------------------------------------------------
app = Flask(__name__)


@app.route("/perform_query/", methods=['POST'])
def perform_query() -> Response:
    """
    Route to form request from body by POST request method
    :return: response with overwritten data
    """
    args: Optional[dict] = request.json

    try:
        if not args:
            raise EmptyArgs

        else:
            file_path = os.path.join(DATA_DIR, args['filename'])
            if not os.path.exists(file_path):
                raise FileNotFoundError

            else:
                user_request = UserRequest(args)

                with open(file_path, encoding='utf8') as f:
                    result: str = '\n'.join(user_request.get_result(f))

            return app.response_class(result, content_type="text/plain")

    except (EmptyArgs, SortValue, MapValue, LimitValue, WrongArgs, FileNotFoundError, IndexError, TypeError) as e:
        abort(400, f'{e}')


if __name__ == '__main__':
    app.run(port=5050, debug=True)

