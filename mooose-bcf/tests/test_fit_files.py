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
    assert rows[6279]['altitude'] == 106.39999999999998
    assert rows[6279]['distance'] == 131983.66
    assert rows[6279]['effort'] == '20210822063125'
    assert rows[6279]['enhanced_altitude'] == 106.39999999999998
    assert rows[6279]['enhanced_speed'] == 0.551
    assert rows[6279]['heart_rate'] == 131
    assert rows[6279]['position_lat'] == 676720078
    assert rows[6279]['position_long'] == -44990738
    assert rows[6279]['speed'] == 0.551
    assert rows[6279]['temperature'] == 14


def _get_file_bytes_contents(file_path: str) -> dict:
    script_dir = os.path.dirname(__file__)

    abs_file_path = os.path.join(script_dir, file_path)
    with open(abs_file_path, "rb") as file:
        file_contents = file.read()

    return file_contents
