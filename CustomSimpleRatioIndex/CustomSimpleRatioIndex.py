import numpy as np

from resononhyperspectral import EnviType

from src.lib.resonon.core.data.cube import Cube
from src.lib.resonon.utils.spec import SpecWavelength
from src.apps.spectronon.workbench.plugin import CubePlugin


class CustomSimpleRatioIndex(CubePlugin):
    """Calculate a Simple Ratio Index using custom wavelengths"""
    defaultRenderer = "SingleBand"
    label = "Custom Simple Ratio Index"
    tooltip = "Calculate a Simple Ratio Index using custom wavelengths."
    documentation = """
        **Description:**
        
        Calculate a custom simple ratio index for each pixel, defined as:
        
        .. math::
            SRI = \\frac{B_{1}}{B_{2}}
        
        If B_{2} is zero for any pixels, the return value of those pixels will be set to zero.
        
        **Usage:**
        
        *First Band:* The wavelength of the first band (numerator).
        
        *Second Band:* The wavelength of the second band (denominator).
        
        **Outputs:**
        
        * A floating point cube of the simple ratio.
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
        self.first_wavelength = SpecWavelength('First Band', self.datacube, defaultValue=800)
        self.second_wavelength = SpecWavelength('Second Band', self.datacube, defaultValue=680)

    def action(self):
        bip_view = self.datacube.bip()
        b1 = bip_view.wavelength_to_band(self.first_wavelength.value)
        b2 = bip_view.wavelength_to_band(self.second_wavelength.value)

        band_one = bip_view[:, :, b1:b1+1].copy_data(dtype=EnviType.FLOAT32)
        band_two = bip_view[:, :, b2:b2+1].data()

        # Avoid division by zero
        result = np.divide(band_one, band_two, out=np.zeros_like(band_one), where=band_two != 0)

        newcube = Cube.from_metadata(self.result_header())
        newcube.set_data(result)

        return newcube

