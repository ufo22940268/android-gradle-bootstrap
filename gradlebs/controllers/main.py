from flask import Blueprint, render_template, flash, request, redirect

from gradlebs import cache
from gradlebs.forms import MyForm
from gradlebs import packages

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route('/wtform', methods=['GET', 'POST'])
def wtform():
    form = MyForm()

    if request.method == 'GET':
        return render_template('wtform_example.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            flash("The form was successfully submitted", 'success')
        else:
            flash("There was a problem submitting the form!", 'danger')
        return render_template('wtform_example.html', form=form)

@main.route('/customize', methods=['GET'])
def customize_handler():
    package_name = request.args['package_name']
    app_name = request.args['app_name']
    file_name = packages.customize(package_name, app_name)
    file_url = '/static/public/zipfiles/' + file_name
    return redirect(file_url, code=302)
