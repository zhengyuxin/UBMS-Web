import os
import sys

from flask import render_template, session, redirect, url_for, current_app, abort
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm
from .forms import form_factory
from Config.PlatformPdo2 import PlatformPdo2

platformpdo2_obj = None

@main.route('/openproject')
def open_project():
    project_name = ''
    project_path = ''
    global platformpdo2_obj
    app = current_app._get_current_object()
    if project_name:
        pass
    else:
        project_path = app.config['BIM_PATH']
        
    platformpdo2_obj = PlatformPdo2()
    
    if platformpdo2_obj.OpenProject(project_path):
        print 'success to open project %s' % project_path
        return redirect(url_for('.index'))
    else:
        print 'fail to open project %s' % project_path
        return render_template('open_project.html', open_project_result='fail to open project %s' % project_path)
    

@main.route('/', methods=['GET', 'POST'])
def index():
    app = current_app._get_current_object()
    global platformpdo2_obj
    
    if not platformpdo2_obj:
        return redirect(url_for('.open_project'))
    else:
        pass
    
    questions = platformpdo2_obj.Get('Question')
    QuestionsForm, default_value_dict = form_factory(questions)
    questions_form = QuestionsForm(**default_value_dict)
    if questions_form.validate_on_submit():
        
        return redirect(url_for('.index'))
    
    return render_template('index.html',
                           form=questions_form)

@main.route('/hardware', methods=['GET', 'POST'])
def hardware():
    app = current_app._get_current_object()
    global platformpdo2_obj
    
    if not platformpdo2_obj:
        abort(404)
    else:
        pass
    
    hardware_bom = platformpdo2_obj.Get('PlatformBillOfMaterials')
    hardware_inventory = platformpdo2_obj.Get('PlatformInfInventory')
    
    HardwareForm, default_value_dict = form_factory(hardware_bom + hardware_inventory)
    hardware_form = HardwareForm(**default_value_dict)
    
#     if hardware_form.validate_on_submit():
#         
#         return redirect(url_for('hardware'))
    
    return render_template('table_form.html',
                           form=hardware_form)

@main.route('/peripheral', methods=['GET', 'POST'])
def peripheral():
    app = current_app._get_current_object()
    global platformpdo2_obj
    
    if not platformpdo2_obj:
        abort(404)
    else:
        pass
    
    peripheral_bom = platformpdo2_obj.Get('PeripheralBillOfMaterials')
    peripheral_inventory = platformpdo2_obj.Get('PeripheralInfInventory')
    
    PeripheralForm, default_value_dict = form_factory(peripheral_bom + peripheral_inventory)
    peripheral_form = PeripheralForm(**default_value_dict)
    
#     if peripheral_form.validate_on_submit():
#         
#         return redirect(url_for('peripheral'))
    
    return render_template('table_form.html',
                           form=peripheral_form)

@main.route('/connector', methods=['GET', 'POST'])
def connector():
    app = current_app._get_current_object()
    global platformpdo2_obj
    
    if not platformpdo2_obj:
        abort(404)
    else:
        pass
    
    connector_bom = platformpdo2_obj.Get('ConnectorBillOfMaterials')
    connector_inventory = platformpdo2_obj.Get('ConnectorInfInventory')
    
    HardwareForm, default_value_dict = form_factory(connector_bom + connector_inventory)
    hardware_form = HardwareForm(**default_value_dict)
    
#     if hardware_form.validate_on_submit():
#         
#         return redirect(url_for('hardware'))
    
    return render_template('table_form.html',
                           form=hardware_form)
    
@main.route('/firmware', methods=['GET', 'POST'])
def firmware():
    app = current_app._get_current_object()
    global platformpdo2_obj
    
    if not platformpdo2_obj:
        abort(404)
    else:
        pass
    platformpdo2_obj.FindModuleSolution()
    global_module_tie_list = platformpdo2_obj.Get('ModuleTie')
    firmware_list = platformpdo2_obj.Get('FirmwareModule')
    
#     FirmwareForm, default_value_dict = form_factory(firmware_list)
#     firmware_form = FirmwareForm()
    
#     if hardware_form.validate_on_submit():
#         
#         return redirect(url_for('hardware'))
#     firmwares = platformpdo2_obj.GetModuleSolution()
    firmwares = [(i.GetDisplayName(), i.GetModule()) for i in firmware_list]
    moduleties = [(i.GetDisplayName(),i.GetCurrentValue()) for i in global_module_tie_list]
    
    return render_template('firmware.html',
                           firmwares=firmwares, moduleties=moduleties)
    