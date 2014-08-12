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

class RequiredIf(validators.Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)

class InputForm(Form):
    name = wtforms.TextField('Name', validators = [validators.InputRequired()])
    birthday = wtforms.DateField('Birthday', format='%m/%d/%Y', validators = [validators.InputRequired()])
    school = wtforms.TextField('School', validators = [validators.InputRequired()])

    grade_opts = [(str(i), str(i)) for i in range(1,13)]
    grade_opts.insert(0, ('K', 'K'))
    grade = wtforms.SelectField('Grade', coerce=str, choices=grade_opts, validators = [validators.InputRequired()])

    examiner = wtforms.TextField('Examiner', validators = [validators.InputRequired()])


@app.route('/', methods=['GET', 'POST'])
def report_form():
    form = InputForm()

    if form.validate_on_submit():
        return render_template('report.html', form=form)
    else:
        return render_template('input_form.html', form=form)


if __name__ == '__main__':
    app.run()
