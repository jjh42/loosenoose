from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template
import logging
import os
from solver import Dictionary

class SolverPage(webapp.RequestHandler):
    def render_template(self, template_name, values={}):
        logging.info('Rendering %s with values %s' % (template_name, str(values)))
        path = os.path.join(os.path.dirname(__file__), template_name)
        self.response.out.write(template.render(path, values))
        
    def get(self):
        word = self.request.get('word')
        results = {}
        if word:
            results['word'] = word
            logging.info('Guessing word %s' % word)
            d = Dictionary(word)
            logging.info('Predictions %s' % str(d.predictions))
            # Generate some fontsizes
            results['predictions'] = map(lambda x: (x[0], x[1], 40*(x[1]/d.predictions[0][1]),
                                                    10*(x[1]/d.predictions[0][1])),
                                         d.predictions)
        self.render_template('solver.html', results)


application = webapp.WSGIApplication(
                                     [('/.*', SolverPage),
                                      ],
                                     debug=True)
 
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


