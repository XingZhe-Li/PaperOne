# Load Packages
import os
import flask
import importlib
from gevent import pywsgi

# Program Settings
settings_flask_port = 80
settings_flask_mode = 'production'
settings_flask_host = '0.0.0.0'

# beginning exchange WorkDir
print('[INFO] Changing Working Directory')
PaperOne_root = os.path.dirname(__file__)
print('[INFO] Got Workdir \"{0}\"'.format(PaperOne_root))
os.chdir(PaperOne_root)

# Init Flask as PaperCore
print('[INFO] Initing flask.Flask Core')
PaperCore = flask.Flask(__name__)

# Init PaperLib
class build_Paperlib:
    # Init Object modules
    class build_modules:pass
    modules = build_modules()
    del build_modules
    
    # Init Path Bindings
    def root(url):
        return 'Default Root: {0}'.format(url)
    binds = {'/':root}

    # PaperLib Built-in Methods
    def bind(self,path,method):
        self.binds[path] = method
    def share(self,module_name,module_object):
        exec("self.modules.{0} = module_object".format(module_name))
PaperLib = build_Paperlib()

# Scan Papers
Papers = {}
for paper in os.listdir('./Papers'):
    if os.path.isdir('./Papers/'+paper):
        print('[INFO] Importing \"{0}\"'.format(paper))
        paper_content = importlib.import_module('Papers.{0}'.format(paper))
        Papers[paper] = paper_content
    else:
        print('[ERROR] Paper \"{0}\" is not a directory'.format(paper))

# Build Modules
for paper in Papers:
    if hasattr(Papers[paper],'main'):
        if callable(Papers[paper].main):
            Papers[paper].main(PaperLib)
        else:
            print('[ERROR] \"{0}.main\" is not callable'.format(paper))
    else:
        print('[ERROR] Did not found main in \"{0}\"'.format(paper))

# Bind Papers
@PaperCore.route('/',methods=['GET', 'POST'])
def root():
    return PaperLib.binds['/']('')

@PaperCore.route('/<path:url>',methods=['GET', 'POST'])
def routes(url):
    slash_position = url.find('/',0)
    if slash_position==-1:
        if url in PaperLib.binds:
            return flask.redirect(url+'/')
        else:
            return PaperLib.binds['/'](url)
    else:
        if url[:slash_position] in PaperLib.binds:
            return PaperLib.binds[url[:slash_position]](url[slash_position+1:])
        else:
            return PaperLib.binds['/'](url)

# Launch Server
if __name__ == '__main__':
    print('[INFO] Starting PaperOne')
    if settings_flask_mode == 'debug':
        print('[INFO] Running in debug mode')
        PaperCore.run(host=settings_flask_host,port=settings_flask_port,debug=True)
    else:
        print('[INFO] Running in production mode')
        server = pywsgi.WSGIServer((settings_flask_host,settings_flask_port), PaperCore)
        server.serve_forever()