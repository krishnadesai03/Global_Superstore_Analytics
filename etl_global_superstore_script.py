import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_dynamic_df = glueContext.create_dynamic_frame.from_catalog(
    database = "global_superstore_db",
    table_name = "global_superstore_csv",
    transformation_ctx = "source_dynamic_df"
)

cleaned_dynamic_df = DropNullFields.apply(frame = source_dynamic_df)

glueContext.write_dynamic_frame.from_options(
    frame = cleaned_dynamic_df,
    connection_type = "s3",
    connection_options = {
        "path": "s3://global-superstore-krishna-1/processed-data/",
        "partitionKeys": []
    },
    format = "parquet",
    transformation_ctx = "datasink"
)

job.commit()
