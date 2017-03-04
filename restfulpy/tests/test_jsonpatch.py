import unittest

import ujson
from nanohttp import context, action, RestController, Context, configure

from restfulpy.controllers import JsonPatchControllerMixin


class BiscuitsController(RestController):
    @action
    def put(self, id_: int = None):
        result = {}
        result.update(context.form)
        result['id'] = id_
        return result


class SimpleJsonPatchController(JsonPatchControllerMixin, RestController):
    biscuits = BiscuitsController()


class JsonPatchTestCase(unittest.TestCase):
    __configuration__ = '''
    '''

    @classmethod
    def setUpClass(cls):
        configure(init_value=cls.__configuration__)

    def test_jsonpatch_rfc6902(self):
        environ = {
            'REQUEST_METHOD': 'PATCH'
        }
        with Context(environ):
            controller = SimpleJsonPatchController()
            context.form = [
                {"op": "put", "path": "biscuits/1", "value": {"name": "Ginger Nut"}},
            ]
            result = ujson.loads(controller())
            self.assertEqual(len(result), 1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()