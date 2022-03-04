import os

from fit_files import read_fit_file


def test_fit_files_happy_path():
    # Arrange
    fit_file_name = "../../data/sample.fit"
    activity_id = "20210822063125"
    contents = _get_file_bytes_contents(fit_file_name)

    # Act
    rows = read_fit_file(activity_id, contents)
    assert len(rows) == 6280
    assert rows[6279] == {
        'altitude': 106.39999999999998,
        'distance': 131983.66,
        'effort': '20210822063125',
        'enhanced_altitude': 106.39999999999998,
        'enhanced_speed': 0.551,
        'heart_rate': 131,
        'position_lat': 676720078,
        'position_long': -44990738,
        'speed': 0.551,
        'temperature': 14,
        'time': 1632051220.0
    }


def _get_file_bytes_contents(file_path: str) -> dict:
    script_dir = os.path.dirname(__file__)

    abs_file_path = os.path.join(script_dir, file_path)
    with open(abs_file_path, "rb") as file:
        file_contents = file.read()

    return file_contents
