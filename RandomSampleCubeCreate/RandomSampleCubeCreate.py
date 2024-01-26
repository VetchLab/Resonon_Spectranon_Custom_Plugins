import random
import numpy

from resononhyperspectral import Interleave
from src.apps.spectronon.workbench.plugin import SelectPlugin
from src.lib.resonon.utils.spec import Spec, SpecInt
from src.lib.resonon.core.data.cube import Cube

class CreateCubeFromRandomSelection(SelectPlugin):
    """
    Creates a new cube from a random selection of pixels in the current selection,
    disregarding spatial information if needed.
    """

    label = "Create Cube From Random Selection"
    menuPosition = 0
    tooltip = "Create new cube from random selection."

    def setup(self):
        self.new_name = Spec("New Name", defaultValue="{}-RandomSelection".format(self.datacube.label))
        self.pixel_count = SpecInt("Pixels", minval=1, maxval=numpy.iinfo(numpy.int32).max, defaultValue=1)

    def action(self):
        try:
            start_sample, start_line, end_sample, end_line = self.rect
        except (AttributeError, TypeError):
            # case of non-rectangular selection
            pointlist = numpy.array(self.pointlist).astype('uint16')
            if len(pointlist) < self.pixel_count.value:
                raise ValueError("Requested pixel count exceeds available pixels in the selection.")

            random_indices = random.sample(range(len(pointlist)), self.pixel_count.value)
            pointlist = pointlist[random_indices]

            new_data = self.datacube.bip().data()[pointlist[:, 1], pointlist[:, 0], :]
        else:
            if (end_line - start_line) * (end_sample - start_sample) < self.pixel_count.value:
                raise ValueError("Requested pixel count exceeds available pixels in the selection.")

            samples = numpy.random.randint(start_sample, end_sample, self.pixel_count.value)
            lines = numpy.random.randint(start_line, end_line, self.pixel_count.value)

            new_data = self.datacube.bip().data()[lines, samples, :]

        if new_data.ndim == 2:  
            new_data = new_data[numpy.newaxis, :]  # Add an extra dimension

        new_cube = Cube.from_array(new_data, interleave=Interleave.BIP)
        header = self.datacube.bip().copy_header()
        keys = new_cube.header_keys
        for key in header:
            if key not in keys:
                new_cube.set_header_value(key, header[key])

        new_cube.label = self.new_name.value
        self.wb.addCube(new_cube)

        # also return the new cube
        return new_cube
