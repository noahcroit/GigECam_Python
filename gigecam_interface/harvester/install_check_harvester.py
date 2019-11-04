from harvesters.core import Harvester



# Harvester object
h = Harvester()

# Add .cti file from mvGenTL installation path
cti_file_path = 'C:/MATRIX_VISION/mvIMPACT_Acquire/bin/x64/mvGenTLProducer.cti'
h.add_cti_file(cti_file_path)

# Update connected hardwares (if there are connected device(s), device's info is read
h.update_device_info_list()
print(h.device_info_list)