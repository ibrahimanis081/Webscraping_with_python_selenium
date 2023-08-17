import configparser
import great_expectations as gx

# Read the configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Access the database credentials
db_host = config['database']['host']
db_port = config['database']['port']
db_username = config['database']['username']
db_password = config['database']['password']
db_name = config['database']['database_name']

connection_string = (
    f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
)

context = gx.get_context()
print("Context created")

context.add_or_update_expectation_suite("my_expectation_suite")

datasource = context.sources.add_sql(
    name="my_datasource", connection_string=connection_string
)

print("connected to data source")

datasource = context.get_datasource("my_datasource")
table_asset = datasource.add_table_asset(name="my_asset", table_name="us_accredited_online_colleges")
batch_request = table_asset.build_batch_request()

validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="my_expectation_suite",
)


validator.expect_column_values_to_not_be_null(column="s/n")
column_check = validator.expect_table_column_count_to_equal(5)

print(column_check)

validator.save_expectation_suite()


context.build_data_docs()
context.open_data_docs()



