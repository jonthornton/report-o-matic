from flask import Flask, request, render_template, flash, url_for
from flask.ext.wtf import Form
import wtforms
from wtforms import validators

app = Flask(__name__)
app.config.from_envvar('REPORT_O_MATIC_SETTINGS')

def describe_score(score, low=0, high=100):
    buckets = ['bad', 'basic', 'bitchin\'']
    index = int((float(score - low) / (high - low)) * len(buckets))
    return buckets[min(index, len(buckets) - 1)]

app.jinja_env.globals.update(describe_score=describe_score)

class DummyForm(Form):
    name = wtforms.TextField('Your name', validators = [validators.InputRequired()])
    score = wtforms.IntegerField('Score (0-100)', validators = [validators.InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def report_form():
    form = DummyForm()

    if form.validate_on_submit():
        return render_template('report.html', form=form)
    else:
        return render_template('input_form.html', form=form)


if __name__ == '__main__':
    app.run()
