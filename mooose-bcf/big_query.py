from google.cloud.bigquery import Client


def put_rows(rows, project, dataset_name, table_name):
    client = Client(project)
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)
    table = client.get_table(table_ref)
    errors = client.insert_rows_json(table, rows)
    print(errors)
