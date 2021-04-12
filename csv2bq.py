from __future__ import absolute_import
import argparse
import logging
import re
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import os
import json

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcp-expert-sandbox-allen-c1fcfd19238a.json"

class DataIngestion:

    def __init__(self,schema): 
        self.schema = tuple(schema)

    def parse_method(self, string_input):
        values = re.split(",",
                          re.sub('\r\n', '', re.sub(u'"', '', string_input)))
        row = dict(
            zip(self.schema,
                values))
        return row


def run(argv=None):
    """The main function which creates the pipeline and runs it."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input',
        dest='input',
        required=True,
        help='Input file to read. This can be a local file or '
        'a file in a Google Storage Bucket.')

    # This defaults to the lake dataset in your BigQuery project. You'll have
    # to create the lake dataset yourself using this command:
    # bq mk lake
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        help='Output BQ table to write results to.')


    parser.add_argument('--temp_bucket',
                        dest='temp_bucket',
                        required=True,
                        help='temp bucket name.')


    parser.add_argument('--schema',
                        dest='schema',
                        required=True,
                        help='data schema json format.')
    

    parser.add_argument('--credential',
                        dest='credential',
                        required=True,
                        help='credential json key.')


    parser.add_argument('--skip_csv_lines',
                        dest='skip_csv_lines',
                        type=int,
                        required=False,
                        help='skip csv lines.',
                        default=1)

    # Parse arguments from the command line.
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_args += ["--runner=DataflowRunner", 
                      "--save_main_session", 
                      #"--staging_location=gs://%s/staging" % (known_args.temp_bucket),
                      "--temp_location=gs://%s/temp" % (known_args.temp_bucket)]

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = known_args.credential

    schema = json.loads(known_args.schema)
    
    # DataIngestion is a class we built in this script to hold the logic for
    # transforming the file into a BigQuery table.
    data_ingestion = DataIngestion(schema)

    # Initiate the pipeline using the pipeline arguments passed in from the
    # command line. This includes information such as the project ID and
    # where Dataflow should store temp files.
    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    (
     p | 'Read from a File' >> beam.io.ReadFromText(known_args.input,
                                                  skip_header_lines=known_args.skip_csv_lines)
    
     # This stage of the pipeline translates from a CSV file single row
     # input as a string, to a dictionary object consumable by BigQuery.
     # It refers to a function we have written. This function will
     # be run in parallel on different workers using input from the
     # previous stage of the pipeline.
     | 'String To BigQuery Row' >>
     beam.Map(lambda s: data_ingestion.parse_method(s))
     | 'Write to BigQuery' >> beam.io.Write(
         beam.io.BigQuerySink(
             # The table name is a required argument for the BigQuery sink.
             # In this case we use the value passed in from the command line.
             known_args.output,
             # Here we use the simplest way of defining a schema:
             # fieldName:fieldType

             schema=','.join("%s:%s" % (str(k), str(v)) for (k, v) in schema.items()),

             # Creates the table in BigQuery if it does not yet exist.
             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
             # Deletes all data in the BigQuery table before writing.
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)))
    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
