from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import template
import os
import logging

class SolverPage(webapp.RequestHandler):
    def render_template(self, template_name, values={}):
        logging.info('Rendering %s with values %s' % (template_name, str(values)))
        path = os.path.join(os.path.dirname(__file__), template_name)
        self.response.out.write(template.render(path, values))
        
    def get(self):
        self.render_template('solver.html', {})


application = webapp.WSGIApplication(
                                     [('/.*', SolverPage),
                                      ],
                                     debug=True)
 
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


