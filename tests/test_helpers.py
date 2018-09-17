import matplotlib
matplotlib.use('agg')
import unittest
import numpy as np
from hypothesis import given, strategies as st
from hypothesis.extra import numpy as st_np

import sys
import mock

while True:
    # try to import CameraTransform
    try:
        import CameraTransform as ct
    # if an import error occurs
    except ImportError as err:
        # get the module name from the error message
        name = str(err).split("'")[1]
        print("Mock:", name)
        # and mock it
        sys.modules.update((mod_name, mock.MagicMock()) for mod_name in [name])
        # then try again to import it
        continue
    else:
        break

points = st_np.arrays(dtype="float", shape=st.tuples(st.integers(2, 2), st.integers(0, 100)), elements=st.floats(0, 10000))

class TestHelpers(unittest.TestCase):

    @given(st.integers(-90, 90), st.integers(0, 59), st.integers(0, 59))
    def test_formatGPS(self, deg, min, sec):
        return
        # test with N/S, W/E
        fmt = "%2d° %2d' %6.3f %s"
        degs = (abs(deg)+min/60+sec/(60*60))*(1-2*(deg<0))
        lat, lng = ct.formatGPS(degs, degs, format=fmt)
        if deg < 0:
            self.assertEqual(lat, fmt % (abs(deg), min, sec, "S"))
            self.assertEqual(lng, fmt % (abs(deg), min, sec, "W"))
        else:
            self.assertEqual(lat, fmt % (abs(deg), min, sec, "N"))
            self.assertEqual(lng, fmt % (abs(deg), min, sec, "E"))

        # test with +- sign
        fmt = "%2d° %2d' %6.3f"
        lat, lng = ct.formatGPS(degs, degs, format=fmt)
        self.assertEqual(lat, fmt % (deg, min, sec))

        # test as just one value
        fmt = "%2f.2°"
        lat, lng = ct.formatGPS(degs, degs, format=fmt)
        self.assertEqual(lat, fmt % (degs))


if __name__ == '__main__':
    unittest.main()


