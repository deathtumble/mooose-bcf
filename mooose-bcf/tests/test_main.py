import os
import json

from mock import patch, Mock

from main import hello_gcs


@patch("main.read_file")
@patch("main.put_rows")
def test_main_happy_path(put_rows, read_file):
    # Arrange
    gpx_file_name = "../../data/activity_187550148.gpx"
    read_file.return_value = _get_file_contents(gpx_file_name)
    event = _get_json_file_contents("event.json")
    context = Mock()

    # Act
    hello_gcs(event, context)

    # Assert
    read_file.assert_called_with("bcf", "activity_187550148.gpx")


def _get_file_contents(file_path: str) -> dict:
    script_dir = os.path.dirname(__file__)

    abs_file_path = os.path.join(script_dir, file_path)
    with open(abs_file_path) as file:
        file_contents = file.read()

    return file_contents


def _get_json_file_contents(file_path: str) -> dict:
    script_dir = os.path.dirname(__file__)

    abs_file_path = os.path.join(script_dir, file_path)
    with open(abs_file_path) as file:
        file_contents = json.loads("".join(file.readlines()))

    return file_contents
