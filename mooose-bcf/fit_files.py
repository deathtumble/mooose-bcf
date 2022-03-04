from io import BytesIO

import fitparse


def read_fit_file(activity_id, contents):
    file = BytesIO(contents)

    fitfile = fitparse.FitFile(file)

    rows = []
    for record in fitfile.get_messages("record"):
        row = {}
        rows.append(row)
        row["effort"] = activity_id

        for data in record:
            if not data.name.startswith("unknown"):
                if data.name == "timestamp":
                    row["time"] = data.value.timestamp()
                else:
                    row[data.name] = data.value

    return rows
