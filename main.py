#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import os
from google.appengine.ext.webapp import template

import cgi
import urllib
import csv

from google.appengine.api.urlfetch_errors import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        url = cgi.escape(self.request.get('url'))
        template_values = {
          'url': url
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
        s = template.render(path, template_values)
        self.response.out.write(s)

    def post(self):

        errors = ""

        # read request parameter, get contents
        url = cgi.escape(self.request.get('url'))
        try:
          f = urllib.urlopen(url)
          contents = f.read()
        except DownloadError, err:
          errors = 'url is invalid'

        # parse csv
        errpos = 0
        if errors == "":
          reader = csv.reader(contents)
          try:
            for row in reader:
               errpos = reader.line_num
            errors = 'OK'
          except csv.Error, e:
            errors = ('column %d: %s' % (errpos, e))

        template_values = {
          'url': url,
          'errors': errors,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/form.html')
        s = template.render(path, template_values)
        self.response.out.write(s)


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
