from src.lib.resonon.utils.spec import SpecBool, SpecInt, SpecDirectory
from src.apps.spectronon.workbench.plugin import CubePlugin
from scipy import stats
from src.lib.resonon.core.data.cube import Cube
import numpy as np
import csv
import os

class BandSummaryAuto(CubePlugin):
    defaultRenderer = 'SingleBandColormap'
    label = "Band Summary Statistics Auto Version V2"
    tooltip = "Automatically calculates and exports summary statistics for all bands of a datacube."
    documentation = "[Your existing documentation string]"

    def setup(self):
        self.ignore_zeros = SpecBool('Ignore Zeros?', False)
        self.output_decimal_places = SpecInt('Output Decimal Places', 0, 20, 1, 4)
        self.output_directory = SpecDirectory("Output Directory", defaultValue=os.getcwd())

    def action(self):
        stats_csv = []

        for band in range(self.datacube.bands):
            band_data = self.datacube.get_band(band).flatten()
            if self.ignore_zeros.value:
                band_data = band_data[np.nonzero(band_data)]

            stats_dict = {
                'wavelength': self.datacube.wavelengths[band],
                'minimum': np.min(band_data),
                '25th percentile': np.percentile(band_data, 25),
                'median': np.median(band_data),
                'mean': np.mean(band_data),
                '75th percentile': np.percentile(band_data, 75),
                'maximum': np.max(band_data),
                'std': np.std(band_data),
                'variance': np.var(band_data),
                'skew': stats.skew(band_data),
                'kurtosis': stats.kurtosis(band_data)
            }
            stats_csv.append(stats_dict)

        self.export_to_csv(stats_csv)

        # Return a copy of the original cube as the result
        return self.datacube.copy()

    def export_to_csv(self, stats_csv):
        filename = os.path.join(self.output_directory.value, "band_summary_statistics.csv")
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = list(stats_csv[0].keys())
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writeheader()
            for row in stats_csv:
                csvwriter.writerow(row)

        self.wb.postMessage(f"Band summary statistics exported to {filename}")
