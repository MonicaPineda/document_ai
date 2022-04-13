import google.auth as google_auth
from google.cloud import documentai_v1beta3 as documentai
import re
from collections import OrderedDict

#from google.oauth2 import service_account
#import os



class DocumentProcessor:
   
    def __init__(self,project_id:str,location:str, processor_id:str, credentials_path:str):

        self.project_id=project_id 
        self.location=location 
        self.processor_id=processor_id
        self.credentials_path=credentials_path          

    @property
    def credentials(self):
        return google_auth.load_credentials_from_file(self.credentials_path)[0]



    def online_process(self, file_path):
        # Process Document Function

        client = documentai.DocumentProcessorServiceClient(credentials=self.credentials)
        name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}" #doc_ai 
        print(name)
        with open(file_path, "rb") as image:
            image_content = image.read()
        # Read the file into memory
        document = {"content": image_content, "mime_type": "application/pdf"}
        # Configure the process request
        request = {"name": name, "document": document}
        result = client.process_document(request=request)
        return result.document

    def batch_process():
        return


