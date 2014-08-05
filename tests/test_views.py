import unittest
from flask import current_app
from app.main import views

class TestViewsFunction(unittest.TestCase):

	def setUp(self):
		self.tree = {'IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Cpu\\E6xx\\E640AtomProcessor.inf|BomModuleInf_22': {\
						('BomModuleInf_22', 'GPIOSUS5', 'BomModuleInf_2', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Led\\Led.inf|BomModuleInf_2', u'LED Header'], \
						('BomModuleInf_22', 'SPI', 'BomModuleInf_20', 'SPI'): ['Leaf', 'WinbondFlashHardwarePkg_7CF8BC33-96F2-4564-B2F1-9CD9F6B30BEA_0.10\\W25Q32FV\\W25Q32FvSpiFlash.inf|BomModuleInf_20', u'Winbond W25Q32FV 32Mb SPI flash'], \
						('BomModuleInf_22', 'PCIE0', 'BomModuleInf_19', 'PCIE'): ['Child', 'IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Chipset\\EG20T\\Eg20t.inf|BomModuleInf_19', u'Intel(R) Platform Controller Hub EG20T', {\
							('BomModuleInf_19', 'USB1', 'BomModuleInf_8', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeA\\UsbTypeA.inf|BomModuleInf_8', u'USB Type A'], \
							('BomModuleInf_19', 'USB0', 'BomModuleInf_7', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeA\\UsbTypeA.inf|BomModuleInf_7', u'USB Type A'], \
							('BomModuleInf_19', 'USBCLIENT', 'BomModuleInf_10', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeMicroB\\UsbTypeMicroB.inf|BomModuleInf_10', u'USB Type Micro B'], \
							('BomModuleInf_19', 'GIGE', 'BomModuleInf_1', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Network\\NetworkRj45\\NetworkRj45.inf|BomModuleInf_1', u'Network RJ45'], \
							('BomModuleInf_19', 'SD0', 'BomModuleInf_5', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Sd\\MicroSdSocket\\MicroSdSocket.inf|BomModuleInf_5', u'uSD Socket']}], \
						('BomModuleInf_22', 'JTAG', 'BomModuleInf_9', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\XdpHeader\\XdpHeader.inf|BomModuleInf_9', u'XDP Header'], \
						('BomModuleInf_22', 'GPIOSUS6', 'BomModuleInf_3', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Led\\Led.inf|BomModuleInf_3', u'LED Header'], \
						('BomModuleInf_22', 'SPI', 'BomModuleInf_11', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\DediProgHeader\\DediProgHeader.inf|BomModuleInf_11', u'DediProg SPI Header'], \
						('BomModuleInf_22', 'MEMORY', 'BomModuleInf_23', 'MEMORY'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Hardware\\Ddr2Memory\\Ddr2Memory.inf|BomModuleInf_23', u'N/A DDR2 Memory'], \
						('BomModuleInf_22', 'AUDIO', 'BomModuleInf_4', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Audio\\AudioJacks\\AudioJacks.inf|BomModuleInf_4', u'Audio Jack'], \
						('BomModuleInf_22', 'SDVO', 'BomModuleInf_13', 'BOARD'): ['Child', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Video\\Hdmi\\Hdmi.inf|BomModuleInf_13', u'HDMI', {\
							('BomModuleInf_13', 'PERIPHERAL', 'BomModuleInf_18', 'VIDEO'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Peripherals\\Monitor\\Monitor.inf|BomModuleInf_18', u'Monitor']}]}}

	def test_find_dict_in_tree_1(self):
		self.assertEqual(views.find_dict_in_tree(self.tree, 'IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Cpu\\E6xx\\E640AtomProcessor.inf|BomModuleInf_22'),\
						['IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Cpu\\E6xx\\E640AtomProcessor.inf|BomModuleInf_22'])

	def test_dict_in_tree_1(self):
		self.assertEqual(views.dict_in_tree(self.tree, 'IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Cpu\\E6xx\\E640AtomProcessor.inf|BomModuleInf_22'),\
						self.tree['IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Cpu\\E6xx\\E640AtomProcessor.inf|BomModuleInf_22'])
		
	def test_dict_in_tree_2(self):
		self.assertEqual(views.dict_in_tree(self.tree, 'IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Cpu\\E6xx\\E640AtomProcessor.inf|BomModuleInf_12'),\
						 None)
				
	def test_dict_in_tree_3(self):
		self.assertEqual(views.dict_in_tree(self.tree, 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Video\\Hdmi\\Hdmi.inf|BomModuleInf_13'),\
						self.tree['IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Cpu\\E6xx\\E640AtomProcessor.inf|BomModuleInf_22'][('BomModuleInf_22', 'SDVO', 'BomModuleInf_13', 'BOARD')][-1])
	
	def test_dict_in_tree_4(self):
		self.assertDictEqual(views.dict_in_tree(self.tree, 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Video\\Hdmi\\Hdmi.inf|BomModuleInf_13'),\
						{('BomModuleInf_13', 'PERIPHERAL', 'BomModuleInf_18', 'VIDEO'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Peripherals\\Monitor\\Monitor.inf|BomModuleInf_18', u'Monitor']})
	
	def test_dict_in_tree_5(self):
		self.assertListEqual(views.dict_in_tree(self.tree, 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeA\\UsbTypeA.inf|BomModuleInf_7'),\
						['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeA\\UsbTypeA.inf|BomModuleInf_7', u'USB Type A'])
	
	def test_dict_in_tree_6(self):
		self.assertDictEqual(views.dict_in_tree(self.tree, 'IntelHardwarePkg_64260E85-B9F0-4fb7-BE5E-0A64607E903A_0.10\\Chipset\\EG20T\\Eg20t.inf|BomModuleInf_19'),\
						{('BomModuleInf_19', 'USB1', 'BomModuleInf_8', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeA\\UsbTypeA.inf|BomModuleInf_8', u'USB Type A'], \
						 ('BomModuleInf_19', 'USB0', 'BomModuleInf_7', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeA\\UsbTypeA.inf|BomModuleInf_7', u'USB Type A'], \
						 ('BomModuleInf_19', 'USBCLIENT', 'BomModuleInf_10', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Usb\\UsbTypeMicroB\\UsbTypeMicroB.inf|BomModuleInf_10', u'USB Type Micro B'], \
						 ('BomModuleInf_19', 'GIGE', 'BomModuleInf_1', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Network\\NetworkRj45\\NetworkRj45.inf|BomModuleInf_1', u'Network RJ45'], \
						 ('BomModuleInf_19', 'SD0', 'BomModuleInf_5', 'BOARD'): ['Leaf', 'HardwarePkg_F9D480FC-75A5-4ac3-B0A4-9D16B61C5263_0.10\\Connectors\\Sd\\MicroSdSocket\\MicroSdSocket.inf|BomModuleInf_5', u'uSD Socket']})
	
	# TODO: test netlist_2_tree
	def test_netlist_2_tree_1(self):
		# test connections in random order
		pass

	# TODO: test netlist_2_tree
	def test_netlist_2_tree_2(self):
		# test netlist_2_tree when child node is absent
		pass

	# TODO: test netlist_2_tree
	def test_netlist_2_tree_3(self):
		# test netlist_2_tree when leaf node is absent
		pass

if __name__ == '__main__':
    unittest.main()