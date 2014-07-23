import string
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms import BooleanField
from wtforms import Label
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


def form_factory(questions):
    
    default_value_dict = {}
    class DynamicForm(Form):
        pass
        
    for each_question in questions:
        display_format = each_question.GetSuggestedDisplayFormat()
        current_value  = each_question.GetCurrentValue()
        if each_question.GetType() in ['Question', 'PcdSettings']:
            label = each_question.GetPcdGuidName().replace('.','_')
        else:
            label = each_question.GetModule()
            
        default_value_dict[label] = current_value
        if display_format in ['BOOLEAN'] or isinstance(current_value, bool):
            setattr(DynamicForm, label, BooleanField(each_question.GetDisplayName()))                
        elif display_format in ['ENUM']:
            pass
        else:
            setattr(DynamicForm, label, Label(label, each_question.GetDisplayName()))                
        
#     setattr(DynamicForm, 'Next', SubmitField())
    
    return DynamicForm, default_value_dict