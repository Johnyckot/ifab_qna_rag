if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from sentence_transformers import SentenceTransformer
import hashlib

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    model_name = 'all-mpnet-base-v2'

    model = SentenceTransformer(model_name)

    docs_transformed = []

    cnt = 0

    for doc in data :
        # calculate hash for the doc, which is used as Id
        hash_str = doc['url'] + doc['h1'] + doc['h2'] + doc['h3'] + doc['text']
        hash_val = hashlib.md5(hash_str.encode('utf-8')).hexdigest()
        doc['id'] = hash_val        
        doc['embedding'] = model.encode(doc['text']).tolist()

        d ={'id':doc['id']
            ,'url':doc['url']
            ,'h1':doc['h1']
            ,'h2':doc['h2']
            ,'h3':doc['h3']
            ,'text':doc['text']
            ,'full_text':doc['full_text']
            ,'embedding':doc['embedding']
        }

        docs_transformed.append(d)


    return docs_transformed


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'