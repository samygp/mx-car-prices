import os
import tornado.ioloop
import tornado.web
from sklearn import linear_model
import modelazo
from json import dumps

modelo = modelazo.ModeloCarros()

root = os.path.dirname(__file__)
port = 54345

class PredictHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            global modelo
            marca_modelo = self.get_argument("marca") + '_' +  self.get_argument("modelo")
            anio = int(self.get_argument("anio"))
            km = int(self.get_argument("km"))
            result = {
                "precio": modelo.predecir(marca_modelo, anio, km)
            }
            self.write(dumps(result))
        except Exception as e:
            print(e)
            self.write_error(e)


def make_app():
    return tornado.web.Application([
        (r"/()", tornado.web.StaticFileHandler, {"path": root, "default_filename": "index.html"}),
        (r"/predict", PredictHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()