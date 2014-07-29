import string
import urllib
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import TextField
from wtforms import Label
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


def form_factory(element_list):
    
    default_value_dict = {}
    class DynamicForm(Form):
        pass
        
    for each_element in element_list:
        display_format = each_element.GetSuggestedDisplayFormat()
        current_value  = each_element.GetCurrentValue()
        display_txt    = each_element.GetDisplayName()
        if each_element.GetType() in ['Question', 'PcdSettings']:
            label = each_element.GetPcdGuidName().replace('.','_')
        else:
            label = urllib.quote(each_element.GetModule())
            
        default_value_dict[label] = current_value
        if display_format:
            if display_format in ['BOOLEAN']:
                setattr(DynamicForm, label, BooleanField(display_txt))
            elif display_format in ['HEXADECIMAL']:
                setattr(DynamicForm, label, IntegerField(display_txt))
            elif display_format in ['OCTAL']:
                setattr(DynamicForm, label, IntegerField(display_txt))
            elif display_format in ['STR']:
                setattr(DynamicForm, label, TextField(display_txt))
            elif display_format in ['UNISTR']:
                setattr(DynamicForm, label, TextField(display_txt))
            elif display_format in ['ENUM']:
                enum_tuples = [(each_element.GetPropertyElement(i), i) for i in each_element.GetPropertyElement()]
                setattr(DynamicForm, label, SelectField(display_txt, choices=enum_tuples))
            elif display_format in ['BITFIELD']:
                pass
            else:
                setattr(DynamicForm, label, Label(label, display_txt))                
        
        else:
            if isinstance(current_value, bool):
                setattr(DynamicForm, label, BooleanField(display_txt))
            else:
                pass

    return DynamicForm, default_value_dict