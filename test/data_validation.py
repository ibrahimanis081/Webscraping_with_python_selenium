import configparser
from logging import exception
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint

# Read the configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Access the database credentials
db_host = config['database']['host']
db_port = config['database']['port']
db_username = config['database']['username']
db_password = config['database']['password']
db_name = config['database']['database_name']

MYSQL_CONNECTION_STRING = (
    f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
)

context = gx.get_context()
print("Context created")

try:
    MySQL_datasource = context.sources.add_sql(
    name="MySQL_datasource", 
    connection_string=MYSQL_CONNECTION_STRING
)
    print("Connected to DataSource")
except Exception as e:
    print(F"Unable to connect to database {e}")
   


MySQL_datasource.add_table_asset(
    name="us_accredited_online_colleges",
    table_name="us_accredited_online_colleges"
)
batch_request = MySQL_datasource.get_asset("us_accredited_online_colleges").build_batch_request()

expectation_suite_name = "mysql_expectation_suite"

context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
)

# expectations
validator.expect_column_to_exist(column="serial_no")
validator.expect_column_values_to_be_unique(column="serial_no")
validator.expect_column_values_to_not_be_null(column="tuition")
validator.expect_table_column_count_to_be_between(5, 10)
validator.expect_column_values_to_be_of_type("tuition", "INTEGER")
validator.save_expectation_suite(discard_failed_expectations=False)

my_checkpoint_name = "mysql_checkpoint"
checkpoint = Checkpoint(
    name=my_checkpoint_name,
    run_name_template="%Y%m%d-%H%M%S-my-run-name-template",
    data_context=context,
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
    action_list=[
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
    ],
)

context.add_or_update_checkpoint(checkpoint=checkpoint)
checkpoint_result = checkpoint.run()

context.open_data_docs()