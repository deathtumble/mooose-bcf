from do_it import convert


def test_convert():
    df = convert(
        "data/activity_187550144.gpx",
        "build/test-reports/output.csv")
    assert df.shape == (1509, 6)
