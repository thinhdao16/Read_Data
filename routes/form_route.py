from flask import Blueprint, render_template, request
from controller.form_controller import load_result_json

form_bp = Blueprint('form', __name__)

@form_bp.route('/form', methods=['GET'])
def form():
    # Render the form page (templates/form.html)
    return render_template('form.html')

@form_bp.route('/analyze', methods=['POST'])
def analyze():
    # Optionally process form field data from request.form if needed
    # Load JSON data from the controller.
    result = load_result_json()
    return render_template('results.html', **result)
