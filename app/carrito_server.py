import os
import tornado.ioloop
import tornado.web
from sklearn import linear_model
import modelazo

modelo = modelazo.ModeloCarros()

root = os.path.dirname(__file__)
port = 54345

class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Ok")

class PredictHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            global modelo
            marca_modelo = self.get_argument("marca") + '_' +  self.get_argument("modelo")
            anio = int(self.get_argument("anio"))
            km = int(self.get_argument("km"))
            self.write(modelo.predecir(marca_modelo, anio, km))
        except Exception as e:
            print(e)
            self.write_error(e)


def make_app():
    return tornado.web.Application([
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": root, "default_filename": "index.html"}),
        (r"/predict(.*)", PredictHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()