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

@main.route('/project/openproject')
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
    

@main.route('/project/', methods=['GET', 'POST'])
def project():
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
    
    return render_template('project.html',
                           form=questions_form)

@main.route('/', methods=['GET', 'POST'])
def index():
        
    return render_template('index.html')

@main.route('/project/hardware', methods=['GET', 'POST'])
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

@main.route('/project/peripheral', methods=['GET', 'POST'])
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


@main.route('/project/connector', methods=['GET', 'POST'])
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

def find_dict_in_tree(tree, bom_path_id, walked_path=[]):
    
    for each_key in tree.keys():
        if each_key == bom_path_id:
            return [each_key]
        
        each_value = tree.get(each_key)
        for each_sub_key in each_value.keys():
            each_sub_value = each_value.get(each_sub_key)            
            if bom_path_id == each_sub_value[1]:
                walked_path.extend([each_key, each_sub_key])
                return walked_path
            elif each_sub_value[0] == "Child":
                find_dict_in_tree({each_sub_value[1]: each_sub_value[-1]}, bom_path_id)
            else:
                pass
        return walked_path

def dict_in_tree(tree, bom_path_id):
    
    for each_key in tree.keys():
        if each_key == bom_path_id:
            return tree.get(each_key)
        
        each_value = tree.get(each_key)
        for each_sub_key in each_value.keys():
            each_sub_value = each_value.get(each_sub_key)            
            if bom_path_id == each_sub_value[1]:
                if each_sub_value[0] == 'Leaf':
                    return each_sub_value
                elif each_sub_value[0] == 'Child':
                    return each_sub_value[-1]
                else:
                    pass
                    
            elif each_sub_value[0] == "Child":
                result = dict_in_tree({each_sub_value[1]: each_sub_value[-1]}, bom_path_id)
                if result:
                    return result
                else:
                    pass
            else:
                pass
        return None


#   convert netlist to n-tree, for the usage of showing connection on WebPage
#   tree is a dictionary
#   key may be one of following:
#       1. tuple:  (parent_id, parent_point, child_id, child_point)
#   value may be one of following:
#       1. list:   ["Leaf", "ModulePath|UniqueId", "DisplayName" ]
#       2. list:   ["Child", "ModulePath|UniqueId", "DisplayName", recursive-tree]

def netlist_2_tree(net_list, connected_bom_dict):

    tree = {}
    processed_bom_id_list = []

    tmp_parent_id = ''

    net_dict = {}
    for net in net_list:
        
        net_keys = sorted(net.keys())
        parent_module_path_id = "%s|%s" % net[net_keys[0]][:2]
        parent_id, parent_point = net[net_keys[0]][1:]
        parent_display_name, available_points = connected_bom_dict.get(parent_module_path_id)

        if parent_point.count('UART0'):
            pass
            
        # parent bom appear for the first time
        if parent_id not in processed_bom_id_list:
            net_dict = {}
            
            tmp_parent_id = parent_id
        # the same dict
        elif tmp_parent_id == parent_id:
            pass
        else:
            net_dict = dict_in_tree(tree, parent_module_path_id)

        for each_key in net_keys[1:]:
            child_id, child_point = net[each_key][1:]
            child_module_path_id = "%s|%s" % net[each_key][:2]
            child_display_name = connected_bom_dict.get(child_module_path_id)[0]
            net_dict[(parent_id, parent_point, child_id, child_point)] = ["Leaf", child_module_path_id, child_display_name]

        node_result = dict_in_tree(tree, parent_module_path_id)
        #===============================================================================================================
        # new tree -- newly generated tree by parsing net
        # tree -- existing dict tree for display connection
        #
        # following condition should be considered
        # 1. new tree may be in tree
        # 2. new tree may be the parent of  tree
        #===============================================================================================================
        if not node_result:
            # TODO: need check whether current tree is parent of existing tree
            if parent_id not in processed_bom_id_list:
                tree[parent_module_path_id] = net_dict
            else:
                pass
        elif isinstance(node_result, dict):
            pass
        elif isinstance(node_result, list):
            #===========================================================================================================
            # if node is Leaf, update it to Child
            #===========================================================================================================
            if node_result[0] == 'Leaf':
                node_result.remove(node_result[0])
                node_result.insert(0, 'Child')
                node_result.append(net_dict)
            else:
                pass
        else:
            pass
        
        processed_bom_id_list.append(parent_id)
    
    return tree

@main.route('/project/connectiontest', methods=['GET', 'POST'])
def connectiontest():
    net_tree = {'IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Cpu\\E6xx\\E640AtomProcessor.inf|BomModuleInf_22': {\
                ('BomModuleInf_22', 'GPIOSUS5', 'BomModuleInf_2', 'BOARD'): ['Child', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Led\\Led.inf|BomModuleInf_2', u'LED Header', {\
                    ('BomModuleInf_2', 'PERIPHERAL', 'BomModuleInf_24', 'LED'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Hardware\\LED\\GreenLed\\GreenLedPeripheral.inf|BomModuleInf_24', u'Green LED']}], \
                ('BomModuleInf_22', 'SPI', 'BomModuleInf_20', 'SPI'): ['Leaf', 'WinbondFlashHardwarePkg_7CF8BC33-96F2-4564-B2F1-9CD9F6B30BEA_0.10\\W25Q32FV\\W25Q32FvSpiFlash.inf|BomModuleInf_20', u'Winbond W25Q32FV 32Mb SPI flash'], \
                ('BomModuleInf_22', 'PCIE0', 'BomModuleInf_19', 'PCIE'): ['Child', 'IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Chipset\\EG20T\\Eg20t.inf|BomModuleInf_19', u'Intel(R) Platform Controller Hub EG20T', {\
                    ('BomModuleInf_19', 'SD0', 'BomModuleInf_5', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Sd\\MicroSdSocket\\MicroSdSocket.inf|BomModuleInf_5', u'uSD Socket'], \
                    ('BomModuleInf_19', 'USB1', 'BomModuleInf_8', 'BOARD'): ['Child', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeA\\UsbTypeA.inf|BomModuleInf_8', u'USB Type A', {\
                        ('BomModuleInf_8', 'PERIPHERAL', 'BomModuleInf_17', 'USB'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Peripherals\\Usb\\UsbKeyboard\\UsbKeyboard.inf|BomModuleInf_17', u'USB Keyboard']}], \
                    ('BomModuleInf_19', 'USBCLIENT', 'BomModuleInf_10', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeMicroB\\UsbTypeMicroB.inf|BomModuleInf_10', u'USB Type Micro B'], \
                    ('BomModuleInf_19', 'GIGE', 'BomModuleInf_1', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Network\\NetworkRj45\\NetworkRj45.inf|BomModuleInf_1', u'Network RJ45'], \
                    ('BomModuleInf_19', 'USB0', 'BomModuleInf_7', 'BOARD'): ['Child', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeA\\UsbTypeA.inf|BomModuleInf_7', u'USB Type A', {\
                        ('BomModuleInf_7', 'PERIPHERAL', 'BomModuleInf_14', 'USB'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Peripherals\\Usb\\UsbFlashDrive\\UsbFlashDrive.inf|BomModuleInf_14', u'USB Flash Drive']}], \
                    ('BomModuleInf_19', 'SATA0', 'BomModuleInf_12', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Sata\\SataInternal\\SataInternal.inf|BomModuleInf_12', u'SATA'], \
                    ('BomModuleInf_19', 'UART0', 'BomModuleInf_21', 'UART'): ['Child', 'FtdiHardwarePkg_21F21580-43F5-4ca6-959D-05EB1E4C26F1_0.10\\Ft230x\\Ft230x.inf|BomModuleInf_21', u'FTDI FT230x Full Speed USB to UART Bridge', {\
                        ('BomModuleInf_21', 'USB', 'BomModuleInf_6', 'BOARD'): ['Child', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeMiniB\\UsbTypeMiniB.inf|BomModuleInf_6', u'USB Type Mini B', {\
                            ('BomModuleInf_6', 'PERIPHERAL', 'BomModuleInf_16', 'USB'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Peripherals\\Usb\\UsbLoggingStandard\\UsbLoggingStandard.inf|BomModuleInf_16', u'USB Logging Console Standard'], \
                            ('BomModuleInf_6', 'PERIPHERAL', 'BomModuleInf_15', 'USB'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Peripherals\\Usb\\UsbConsoleStandard\\UsbConsoleStandard.inf|BomModuleInf_15', u'USB Console']}]}]}], \
                ('BomModuleInf_22', 'JTAG', 'BomModuleInf_9', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\XdpHeader\\XdpHeader.inf|BomModuleInf_9', u'XDP Header'], \
                ('BomModuleInf_22', 'GPIOSUS6', 'BomModuleInf_3', 'BOARD'): ['Child', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Led\\Led.inf|BomModuleInf_3', u'LED Header', {\
                    ('BomModuleInf_3', 'PERIPHERAL', 'BomModuleInf_25', 'LED'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Hardware\\LED\\GreenLed\\GreenLedPeripheral.inf|BomModuleInf_25', u'Green LED']}], \
                ('BomModuleInf_22', 'SPI', 'BomModuleInf_11', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\DediProgHeader\\DediProgHeader.inf|BomModuleInf_11', u'DediProg SPI Header'], \
                ('BomModuleInf_22', 'MEMORY', 'BomModuleInf_23', 'MEMORY'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Hardware\\Ddr2Memory\\Ddr2Memory.inf|BomModuleInf_23', u'N/A DDR2 Memory'], \
                ('BomModuleInf_22', 'AUDIO', 'BomModuleInf_4', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Audio\\AudioJacks\\AudioJacks.inf|BomModuleInf_4', u'Audio Jack'], \
                ('BomModuleInf_22', 'SDVO', 'BomModuleInf_13', 'BOARD'): ['Child', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Video\\Hdmi\\Hdmi.inf|BomModuleInf_13', u'HDMI', {\
                    ('BomModuleInf_13', 'PERIPHERAL', 'BomModuleInf_18', 'VIDEO'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Peripherals\\Monitor\\Monitor.inf|BomModuleInf_18', u'Monitor']}]}}

    return render_template('connection.html', net_tree=net_tree)

def fill_net_tree(bom_path_id, tree, connected_bom_dict):
    for each_key, each_value in tree.iteritems():
        if each_value[0] == 'Child':
            fill_net_tree(each_value[1], each_value[-1], connected_bom_dict)
        else:
            pass

    unconnected_points = set(connected_bom_dict.get(bom_path_id)[1]) - set([i[1] for i in tree.keys()])
    for i in unconnected_points:
        tree[(bom_path_id, i)] = ''

@main.route('/project/connection', methods=['GET', 'POST'])
def connection():
    app = current_app._get_current_object()
    hcp_bom_typelist = ['PeripheralBillOfMaterials','PlatformBillOfMaterials','ConnectorBillOfMaterials']
    global platformpdo2_obj
    
    if not platformpdo2_obj:
        abort(404)
    else:
        pass

    net_list = [net.GetPointDict() for net in platformpdo2_obj.GetConnection()]

    # get all hardware, peripheral and connector(h,c,p) which are in connections
    connected_bom_paths = list(set(["%s|%s" % i[:2] for net in net_list for i in net.values()]))
    # create bom_path:displayname dict
    # key: module_path|UniqueId
    # value: (display name, all available connection point)
    # sample: {'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Video\\Hdmi\\Hdmi.inf|BomModuleInf_13': 
    #          (u'HDMI', ['BOARD', 'PERIPHERAL'])}
    connected_bom_dict = {}
    for each_connected_bom in connected_bom_paths:
        bom_obj_list = platformpdo2_obj.Get(hcp_bom_typelist, each_connected_bom)
        if len(bom_obj_list) == 1:
            display_name = bom_obj_list[0].GetDisplayName()
            connection_point_list = [i[0] for i in bom_obj_list[0].GetPointHelps()]
            connected_bom_dict[each_connected_bom] = (display_name, connection_point_list)
        else:
            abort(404)

    net_tree = netlist_2_tree(net_list, connected_bom_dict)
    for root, tree in net_tree.iteritems():
        fill_net_tree(root, tree, connected_bom_dict)
        net_root =[root, connected_bom_dict.get(root)[0]]
        
    return render_template('connection-colorful.html', net_tree=net_tree, net_root=net_root)
    # return render_template('connection.html', net_tree=net_tree, net_root=net_root)

@main.route('/project/firmware', methods=['GET', 'POST'])
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

@main.route('/project/pcds/<module_path>', methods=['GET', 'POST'])
def pcds(module_path):
    app = current_app._get_current_object()
    global platformpdo2_obj

    if not platformpdo2_obj:
        abort(404)
    else:
        pass

    if module_path == 'global':
        pcdsettings_list = platformpdo2_obj.Get('PcdSettings')
    else:
        pcdsettings_list = platformpdo2_obj.Get('PcdSettings', module_path)

    PcdSettingsForm, default_value_dict = form_factory(pcdsettings_list)
    pcds_form = PcdSettingsForm(**default_value_dict)

    return render_template('pcd_form.html', form = pcds_form)

@main.route('/project/question', methods=['GET', 'POST'])
def question():
    app = current_app._get_current_object()
    global platformpdo2_obj

    if not platformpdo2_obj:
        abort(404)
    else:
        pass

    pcdsettings_list = platformpdo2_obj.Get('Question')
    PcdSettingsForm, default_value_dict = form_factory(pcdsettings_list)
    pcds_form = PcdSettingsForm(**default_value_dict)

    return render_template('question_form.html', form = pcds_form)

