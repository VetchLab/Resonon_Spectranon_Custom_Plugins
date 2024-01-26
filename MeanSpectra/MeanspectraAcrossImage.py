import numpy
from src.apps.spectronon.workbench.plugin import CubePlugin
from src.lib.resonon.core.data.spectrum import Spectrum, ZProfile

class AddMeanOfEntireImageToWorkbench(CubePlugin):
    '''
    Create a spectrum from the mean of the entire image
    '''
    label = "Mean Spectrum of Entire Image"
    menuPosition = 1
    requiresWaves = True
    tooltip = "Create and plot a spectrum from the mean of the entire image."
    documentation = """

                **Description:**

                Create and plot a spectrum from the mean of the entire image. Wavelength metadata must be 
                present for this tool to be available. 
                
                The standard deviation will also be plotted, which can be turned on or off by right clicking on 
                the Spectrum object in the Resource Tree and selecting Show/Hide Standard Deviation.

            """

    def action(self):
        datacube = self.datacube
        array = datacube.bip().data()

        self.std_dev = array.std(axis=(0, 1)).astype('f').flatten()
        self.mean = array.mean(axis=(0, 1)).astype('f').flatten()

        try:
            self.scale = datacube.get_header_value("reflectance scale factor")
        except KeyError:
            self.scale = None
        self.wavelengths = datacube.wavelengths
        if self.wavelengths is not None:
            s = Spectrum.from_array(array=self.mean, wavelengths=self.wavelengths, scale=self.scale, stdev=self.std_dev)
        else:
            s = ZProfile.from_array(array=self.mean, scale=self.scale)

        for meta_name in ("shutter", "gain"):
            try:
                s.set_header_value(meta_name, datacube.get_header_value(meta_name))
            except KeyError:
                pass

        if datacube.label:
            s.set_header_value("original cube file", datacube.label)

        s.label = self.wb.get_next_numbered_spectrum_label(label_prefix="mean-", datacube=datacube)
        self.wb.addSpectrum(s)
        return s

