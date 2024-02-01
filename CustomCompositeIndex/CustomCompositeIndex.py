import numpy as np

from resononhyperspectral import EnviType

from src.lib.resonon.core.data.cube import Cube
from src.lib.resonon.utils.spec import SpecWavelength
from src.apps.spectronon.workbench.plugin import CubePlugin


class CustomCompositeIndex(CubePlugin):
    """Calculate a Composite Index using custom wavelengths"""
    defaultRenderer = "SingleBand"
    label = "Custom Composite Index"
    tooltip = "Calculate a Composite Index using custom wavelengths."
    documentation = """
        **Description:**
        
        Calculate a custom composite index for each pixel, defined as:
        
        .. math::
            CCI = \\frac{B_{0} - B_{1}}{B_{2} / B_{3}}
        
        If B_{2} or B_{3} is zero for any pixels, the return value of those pixels will be set to zero.
        
        **Usage:**
        
        *First Band (Band0):* The wavelength of the first band.
        *Second Band (Band1):* The wavelength of the second band.
        *Third Band (Band2):* The wavelength of the third band.
        *Fourth Band (Band3):* The wavelength of the fourth band.
        
        **Outputs:**
        
        * A floating point cube of the composite index.
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
        self.band0 = SpecWavelength('First Band (Band0)', self.datacube, defaultValue=800)
        self.band1 = SpecWavelength('Second Band (Band1)', self.datacube, defaultValue=680)
        self.band2 = SpecWavelength('Third Band (Band2)', self.datacube, defaultValue=550)
        self.band3 = SpecWavelength('Fourth Band (Band3)', self.datacube, defaultValue=450)

    def action(self):
        bip_view = self.datacube.bip()
        b0 = bip_view.wavelength_to_band(self.band0.value)
        b1 = bip_view.wavelength_to_band(self.band1.value)
        b2 = bip_view.wavelength_to_band(self.band2.value)
        b3 = bip_view.wavelength_to_band(self.band3.value)

        band0 = bip_view[:, :, b0:b0+1].copy_data(dtype=EnviType.FLOAT32)
        band1 = bip_view[:, :, b1:b1+1].data()
        band2 = bip_view[:, :, b2:b2+1].data()
        band3 = bip_view[:, :, b3:b3+1].data()

        # Avoid division by zero for B2 and B3
        band2_band3_ratio = np.divide(band2, band3, out=np.zeros_like(band2), where=band3 != 0)
        
        # Calculate the composite index
        result = np.divide(band0 - band1, band2_band3_ratio, out=np.zeros_like(band0), where=band2_band3_ratio != 0)

        newcube = Cube.from_metadata(self.result_header())
        newcube.set_data(result)

        return newcube
