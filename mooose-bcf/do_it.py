from xml.etree import ElementTree
from dateutil.parser import isoparse
from math import floor

import pandas as pd

CAD_TAG = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}cad"
HR_TAG = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr"
ELE_TAG = "{http://www.topografix.com/GPX/1/1}ele"
TIME_TAG = "{http://www.topografix.com/GPX/1/1}time"
TRKPT_TAG = "{http://www.topografix.com/GPX/1/1}trkpt"


def convert(input_filename, output_filename):
    cols = ["time", "cad", "hr", "ele", "lat", "long"]
    rows = []

    tree = ElementTree.parse(input_filename)
    root = tree.getroot()
    for element in root.iter(TRKPT_TAG):
        time = None
        cad = None
        hr = None
        ele = None
        lat = element.attrib.get("lat")
        long = element.attrib.get("lon")
        for attribute in element.iter():
            if attribute.tag == ELE_TAG:
                ele = floor(float(attribute.text))

            if attribute.tag == TIME_TAG:
                time = isoparse(attribute.text).timestamp()

            if attribute.tag == CAD_TAG:
                cad = attribute.text

            if attribute.tag == HR_TAG:
                hr = attribute.text
        row = {
            "time": time,
            "cad": cad,
            "hr": hr,
            "ele": ele,
            "lat": lat,
            "long": long
        }

        rows.append(row)
        print(row)

    df = pd.DataFrame(rows, columns=cols)

    df.to_csv(output_filename, index=False)

    return df


if __name__ == "__main__":
    convert("data/activity_187550144.gpx", "build/test-reports/output.csv")
