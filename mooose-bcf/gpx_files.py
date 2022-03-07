from xml.etree import ElementTree
from math import floor

from dateutil.parser import isoparse
from numpy import (
    deg2rad, cos, sin, sqrt
)
import pandas


CAD_TAG = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}cad"
HR_TAG = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr"
ELE_TAG = "{http://www.topografix.com/GPX/1/1}ele"
TIME_TAG = "{http://www.topografix.com/GPX/1/1}time"
TRKPT_TAG = "{http://www.topografix.com/GPX/1/1}trkpt"

EARTH_RADIUS = 6371000


def read_gpx_file(activity_id, contents):
    rows = []

    tree = ElementTree.ElementTree(ElementTree.fromstring(contents))
    root = tree.getroot()
    for element in root.iter(TRKPT_TAG):
        time = None
        cad = None
        hr = None
        ele = None
        lat = float(element.attrib.get("lat"))
        long = float(element.attrib.get("lon"))

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

    df = calculate_distances(rows)

    return df.values.tolist()


def calculate_distances(rows):
    df = pandas.DataFrame(rows)
    df['theta'] = deg2rad(df['long'])
    df['phi'] = deg2rad(df['lat'])
    df['x'] = EARTH_RADIUS * cos(df['theta'])*sin(df['phi'])
    df['y'] = EARTH_RADIUS * sin(df['theta'])*sin(df['phi'])
    df['z'] = EARTH_RADIUS * cos(df['phi'])
    df['x2'] = df['x'].shift()
    df['y2'] = df['y'].shift()
    df['z2'] = df['z'].shift()
    df['distance'] = sqrt(
        (df['x2']-df['x'])**2 +
        (df['y2']-df['y'])**2 +
        (df['z2']-df['z'])**2)
    df.drop("theta", 1)
    df.drop("phi", 1)
    df.drop("x", 1)
    df.drop("y", 1)
    df.drop("z", 1)
    df.drop("x2", 1)
    df.drop("y2", 1)
    df.drop("z2", 1)
    return df
