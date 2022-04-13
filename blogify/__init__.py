# blogify/__init__.py
from flask import Flask, render_template

app = Flask(__name__)

@app.errorhandler(404)
def error_404(error):
  return render_template('error_pages/404.html'), 404

@app.errorhandler(403)
def error_403(error):
  return render_template('error_pages/403.html'), 403

from blogify.core.views import core
app.register_blueprint(core)