import numpy as np

from resononhyperspectral import EnviType

from src.lib.resonon.core.data.cube import Cube
from src.lib.resonon.utils.spec import SpecWavelength
from src.apps.spectronon.workbench.plugin import CubePlugin


class CustomDifferenceVegetationIndex(CubePlugin):
    """Calculate a Difference Vegetation Index using custom wavelengths"""
    defaultRenderer = "SingleBand"
    label = "Custom Difference Vegetation Index"
    tooltip = "Calculate a Difference Vegetation Index using custom wavelengths."
    documentation = """
        **Description:**
        
        Calculate a custom difference vegetation index for each pixel, defined as:
        
        .. math::
            CDVI = B_{0} - B_{1}
        
        **Usage:**
        
        *First Band (Band0):* The wavelength of the first band.
        
        *Second Band (Band1):* The wavelength of the second band.
        
        **Outputs:**
        
        * A floating point cube of the difference vegetation index.
        """

    def obsolete_header_keys(self):
        """
        Return a list of header keys that should be removed from the result header if they exist in the parent datacube
        """
        return ["reflectance scale factor", "ceiling", "bit depth", 'wavelength', "wavelength units", "spectral binning"]

    def changed_header_data(self):
        """
        Return a dict of metadata keys/values that should be added or changed in the result datacube
        """
        return {"interleave": "bip",
                "data type": int(EnviType.FLOAT32),
                "bands": 1,
                "band names": [self.label]}

    def setup(self):
        self.first_wavelength = SpecWavelength('First Band (Band0)', self.datacube, defaultValue=800)
        self.second_wavelength = SpecWavelength('Second Band (Band1)', self.datacube, defaultValue=680)

    def action(self):
        bip_view = self.datacube.bip()
        b0 = bip_view.wavelength_to_band(self.first_wavelength.value)
        b1 = bip_view.wavelength_to_band(self.second_wavelength.value)

        band_zero = bip_view[:, :, b0:b0+1].copy_data(dtype=EnviType.FLOAT32)
        band_one = bip_view[:, :, b1:b1+1].data()

        result = band_zero - band_one

        newcube = Cube.from_metadata(self.result_header())
        newcube.set_data(result)

        return newcube
