from xml.etree import ElementTree
from math import floor

from dateutil.parser import isoparse


CAD_TAG = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}cad"
HR_TAG = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr"
ELE_TAG = "{http://www.topografix.com/GPX/1/1}ele"
TIME_TAG = "{http://www.topografix.com/GPX/1/1}time"
TRKPT_TAG = "{http://www.topografix.com/GPX/1/1}trkpt"


def read_gpx_file(activity_id, contents):
    rows = []

    tree = ElementTree.ElementTree(ElementTree.fromstring(contents))
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
            "effort": activity_id,
            "time": time,
            "cad": cad,
            "hr": hr,
            "ele": ele,
            "lat": lat,
            "long": long
        }

        rows.append(row)

    return rows
