import os

from fit_files import read_fit_file


def test_fit_files_happy_path():
    # Arrange
    fit_file_name = "../../data/2021-08-22-06-31-25.fit"
    activity_id = "20210822063125"
    contents = _get_file_bytes_contents(fit_file_name)

    # Act
    rows = read_fit_file(activity_id, contents)
    assert len(rows) == 4387


def _get_file_bytes_contents(file_path: str) -> dict:
    script_dir = os.path.dirname(__file__)

    abs_file_path = os.path.join(script_dir, file_path)
    with open(abs_file_path, "rb") as file:
        file_contents = file.read()

    return file_contents
