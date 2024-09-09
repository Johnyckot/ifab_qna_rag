if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import requests
from bs4 import BeautifulSoup
import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here

    # tbd add functionality to automatically extract linke from the main menu https://www.theifab.com/ ( Selenium should be used??)
    url_list = [
        'https://www.theifab.com/laws/latest/about-the-laws/',
    'https://www.theifab.com/laws/latest/notes-on-the-laws/',
    'https://www.theifab.com/laws/latest/general-modifications/',
    'https://www.theifab.com/laws/latest/guidelines-for-temporary-dismissals/',
    'https://www.theifab.com/laws/latest/guidelines-for-return-substitutes/',
    'https://www.theifab.com/laws/latest/additional-permanent-concussion-substitutions-protocol/',
    'https://www.theifab.com/laws/latest/the-field-of-play/',
    'https://www.theifab.com/laws/latest/the-ball/',
    'https://www.theifab.com/laws/latest/the-players/',
    'https://www.theifab.com/laws/latest/the-players-equipment/',
    'https://www.theifab.com/laws/latest/the-referee/',
    'https://www.theifab.com/laws/latest/the-other-match-officials/',
    'https://www.theifab.com/laws/latest/the-duration-of-the-match/',
    'https://www.theifab.com/laws/latest/the-start-and-restart-of-play/',
    'https://www.theifab.com/laws/latest/the-ball-in-and-out-of-play/',
    'https://www.theifab.com/laws/latest/determining-the-outcome-of-a-match/',
    'https://www.theifab.com/laws/latest/offside/',
    'https://www.theifab.com/laws/latest/fouls-and-misconduct/',
    'https://www.theifab.com/laws/latest/free-kicks/',
    'https://www.theifab.com/laws/latest/the-penalty-kick/',
    'https://www.theifab.com/laws/latest/the-throw-in/',
    'https://www.theifab.com/laws/latest/the-goal-kick/',
    'https://www.theifab.com/laws/latest/the-corner-kick/',
    'https://www.theifab.com/laws/latest/video-assistant-referee-var-protocol/',
    'https://www.theifab.com/laws/latest/fifa-quality-programme/',
    'https://www.theifab.com/laws/latest/glossary/football-bodies/',
    'https://www.theifab.com/laws/latest/glossary/football-terms/',
    'https://www.theifab.com/laws/latest/glossary/referee-terms/',
    'https://www.theifab.com/laws/latest/guidelines/introduction/',
    'https://www.theifab.com/laws/latest/guidelines/positioning-movement-and-teamwork/',
    'https://www.theifab.com/laws/latest/guidelines/body-language-communication-and-whistle/',
    'https://www.theifab.com/laws/latest/guidelines/other-advice/'
    ]



    documents = []

    for url in url_list:

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        h1 = ''
        h2 = ''
        h3 = ''
        text = ''
        h11 = ''

        
        def add_doc(url,h1,h11,h2,h3,text):
            if h1 !='' and text !='':
            # split text into paragraphs
                # for t in text.split('\n'):                
                #     documents.append({'url': url , 'h1': h11 if h11 else h1,'h2':h2, 'h3':h3 ,'text': t , 'full_text':text})
                if h3=='FAQs':
                    h2 = ''
                documents.append({'url': url , 'h1': h11 if h11 else h1,'h2':h2, 'h3':h3 ,'text': text , 'full_text':text})

        elements = soup.findAll(['h1','h2','h3','p'])
        for element in elements:
            # print(  element.text ,element.name )

            # for FAQ section every H2 starts new document (QnA)
            if h3 == 'FAQs' and element.name == 'h2' and text!='':
                add_doc(url,h1,h11,h2,h3,text) 
                text = ''


            if element.name != 'p' and h3 != 'FAQs' :
                if text != '':                
                    add_doc(url,h1,h11,h2,h3,text) 
                    text = ''
                if element.name == 'h1':
                    h1 = element.text
                    h2 = ''
                    h3 = ''

                    span = element.find('span', class_='hidden md:inline')
                    if span:
                        h11 = span.get_text()    

                if element.name == 'h2':
                    h2 = element.text
                    h3 = ''
                if element.name == 'h3':
                    h3 = element.text
            else:
                text = text +  element.text + '\n'       

            
        # append the last doc
        if text !='':
            add_doc(url,h1,h11,h2,h3,text)

    print (len(documents))
    
    return documents


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'