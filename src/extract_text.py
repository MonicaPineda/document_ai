import google.auth as google_auth
from google.cloud import documentai_v1beta3 as documentai
import re
from collections import OrderedDict

#from google.oauth2 import service_account
#import os



class TextExtractor:

    def __init__(self, document, text):
        self.document = document
        self.text = text


    def layout_to_text(self, layout: dict, text: str) -> str:
        """
        Document AI identifies text in different parts of the document by their
        offsets in the entirity of the document's text. This function converts
        offsets to a string.
        """
        response = ""
        # If a text segment spans several lines, it will
        # be stored in different text segments.
        for segment in layout.text_anchor.text_segments:
            start_index = (
                int(segment.start_index)
                if segment in layout.text_anchor.text_segments
                else 0
            )
            end_index = int(segment.end_index)
            response += text[start_index:end_index]
        return response


     
    def get_blocks(self) -> None:
        block_list=[]
        for page in self.document.pages:
            for block in page.blocks:
                block_list.append(self.layout_to_text(block.layout, self.text))
        return block_list  

    def get_paragraphs(self) -> None:
        paragraph_list=[]
        for page in self.document.pages:
            for paragraph in page.paragraphs:
                paragraph_list.append(self.layout_to_text(paragraph.layout, self.text))
        return paragraph_list



    def structure_generator(self, document_blocks, regex):
        is_enumerated = re.compile(regex)
        document_structure = OrderedDict()
        title='Encabezado'
        paragraphs=[]

        for block in document_blocks:
            if (is_enumerated.match(block)):
                document_structure[title]=paragraphs
                title=block
                paragraphs=[]
                #print(block)

            else: 
                paragraphs.append(block)
        document_structure[title]=paragraphs
        return document_structure


    def print_lines(self, lines: dict, text: str) -> None:
        print(f"    {len(lines)} lines detected:")
        first_line_text = layout_to_text(lines[0].layout, text)
        print(f"        First line text: {repr(first_line_text)}")
        last_line_text = layout_to_text(lines[-1].layout, text)
        print(f"        Last line text: {repr(last_line_text)}")

    def print_tokens(self, tokens: dict, text: str) -> None:
        print(f"    {len(tokens)} tokens detected:")
        first_token_text = layout_to_text(tokens[0].layout, text)
        first_token_break_type = tokens[0].detected_break.type_.name
        print(f"       First token text: {repr(first_token_text)}")
        print(f"        First token break type: {repr(first_token_break_type)}")
        last_token_text = layout_to_text(tokens[-1].layout, text)
        last_token_break_type = tokens[-1].detected_break.type_.name
        print(f"        Last token text: {repr(last_token_text)}")
        print(f"        Last token break type: {repr(last_token_break_type)}")

