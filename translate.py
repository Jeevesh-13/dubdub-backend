import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import magic
import os
import goslate
import json

aws_access_key = "AKIAUHNPAIBFR5P2ZZMY"
aws_secret_key = "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"
signature_version = "s3v4"
region_name = "ap-south-1"
aws_bucket = None


class Translate:
    def __init__(self, in_file, lang, in_b_name, out_file, out_b_name):
        #self.loaction = 'C:/Users/DELL/Downloads/'
        self.jsonfile = None
        self.input_bucket_name = in_b_name
        self.output_bucket_name = out_b_name
        self.aws_input_filename = in_file
        self.aws_output_filename = out_file
        self.target_language = lang

    def download_aws(self, access_key=aws_access_key, secret_key=aws_secret_key):
        s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        try:
            s3.Object(self.input_bucket_name, self.aws_input_filename).download_file(self.aws_input_filename)
        except Exception as e:
            logging.error("Exception Occurred",  exc_info=True)
            return False
        print("Download Successful!")
        return True

    def upload_aws(self, access_key=aws_access_key, secret_key=aws_secret_key, object_name=None):
        content_type = magic.from_file(self.aws_output_filename, mime=True)
        if object_name is None:
            object_name = os.path.basename(self.aws_output_filename)

            # Upload the file
        s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        try:
            response = s3_client.upload_file(self.aws_output_filename, self.output_bucket_name, object_name,
                                             ExtraArgs={'ACL': 'public-read', 'ContentType': content_type})
        except ClientError as e:
            logging.error(e)
            return False
        print('Uploaded')
        return True

    def google_translate(self):
        try:
            f = open(self.aws_input_filename)
            input_dictionary = json.load(f)
            output_dictionary = {"groups": []}
            for x in input_dictionary['groups']:
                translated_out = {"lanquage_key": self.target_language}
                lang_key = x['language_key']
                sentence = x[lang_key]
                translated_out[lang_key] = sentence
                gs = goslate.Goslate()
                translated_sentence = gs.translate(sentence, self.target_language)
                translated_out[self.target_language] = translated_sentence
                output_dictionary["groups"].append(translated_out)
            f.close()
            print(output_dictionary)
            with open(self.aws_output_filename, "w") as outfile:
                json.dump(output_dictionary, outfile)
        except Exception as e:
            logging.error("Exception Occurred",  exc_info=True)

        return True

