#The longest word(s) -- longest_words
#Number of words -- wordCounter
#Average word length -- average_length
#Count of unique words -- number_unique_words
#Count of palindromes
# from doc_analyzer import *
import asyncio
from nltk.tokenize import RegexpTokenizer
from .models import FileUpload, FileMetric

def tokenizeString(inputString="Helper method to convert an input string into a list of tokens."):
    """
    Helper method to convert an input string into a list of tokens
    :param inputString: Any one line string that we want to tokenize
    :return: list of token representation of a string with punctuation removed
    """
    # Using RegexpTokenizer to remove punctuation, as word_tokenize leaves the punctuation
    tokenizer = RegexpTokenizer(r"\w+")
    response = [word.lower() for word in tokenizer.tokenize(inputString)] # We will make everything lower case for easy uniqueness processing

    return response


def longestWords(inputList):
    """
    Returns the longest word/words in a string

    :param inputList: Tokens to process
    :return: list with 0 or more elements representing the longest word
    """
    if len(inputList) == 0:
        return None
    longest_word_length = len(max(inputList, key=len))
    response = list()
    for word in inputList:
        if len(word) == longest_word_length:
            response.append(word)
    return response

def wordCounter(inputList):
    """
    Returns the number of words in a list. Trivial, but is its own method in case we want to extend later to accept a list of lists

    :param inputList: Tokens to process
    :return: integer length of the list
    """
    return len(inputList)


def averageLength(inputList):
    """

    :param inputList: Tokens to process
    :return:
    """
    if len(inputList) == 0:
        return None # Cannot divide by 0
    total_length = sum(map(len, inputList)) # get length of each word and then sum the values together
    average = total_length / len(inputList)
    return average

def numberUniqueWords(inputList):
    """
    We're counting the number of unique words in a list

    :param inputList: Tokens to process
    :return:
    """
    setOfWords = set(inputList)
    return len(setOfWords)

def isPalindrome(word):
    """
    Find the palindromes
    :param word:
    :return: True or False if it is a palindrome
    """
    return word == word[::-1]

def numberPalindromes(inputList):
    """
    We're counting the number of palindromes in a list
    :param inputList: Tokens to process
    :return:
    """
    filtered_palindromes = list(filter(isPalindrome, inputList))
    return len(filtered_palindromes)

async def parseFileLine(line):
    """
    Method to be used to asynchronously process file lines

    :param line: Text line to be tokenized
    :return: dictionary with metric results for a single line
    """
    response = {}
    tokens = tokenizeString(line)
    response['longest_words'] = longestWords(tokens)
    response['number_words'] = wordCounter(tokens)
    response['average_length'] = averageLength(tokens)
    response['unique_words'] = set(tokens)
    response['number_unique_words'] = numberUniqueWords(tokens)
    response['number_palindromes'] = numberPalindromes(tokens)
    return response


async def processFile(file_object_to_process):
    """
    Returns
    :param file_object_to_process: Instance of FileUpload model object with .file parameter
    :return:
    """
    tasks = []
    f = file_object_to_process.file.open(mode='rb').readlines()
    for line in f:
        line = line.decode('utf8')
        task = asyncio.ensure_future(parseFileLine(line))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

def runFileMetrics(file_object_to_process):
    """
    Main method to be called to generate file metrics

    :param file_object_to_process: File object to gather metrics on
    :return: returns metrics for a file
    """
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    future = asyncio.ensure_future(processFile(file_object_to_process))
    responses = asyncio.get_event_loop().run_until_complete(future)
    response = {
        'longest_words': list(),
        'number_words': 0,
        'average_length': 0,
        'unique_words': set(),
        'number_unique_words': 0,
        'number_palindromes': 0
    } # What we send back to the user.
    for line in responses:
        if line['number_words'] == 0:
            continue # It was an empty line
        response['longest_words'].extend(line['longest_words']) #We will reduce this at the end
        #For clarity the following combines averages by weighting them according to number of their words
        response['average_length'] = (response['number_words'] * response['average_length'] +  # cumulative average
                                         line['average_length'] * line['number_words']) \
                                        / (line['number_words'] + response['number_words']) # Divided by both counts combined
        response['number_words'] += line['number_words']
        [response['unique_words'].add(_) for _ in line['unique_words']] #Attempt to add all unique words to the existing set
        response['number_palindromes'] += line['number_palindromes']
    response['longest_words'] = list(set(longestWords(response['longest_words']))) #Set to make it unique, coercing to list again to make Flask happy
    response['number_unique_words'] = len(response['unique_words'])
    del response['unique_words'] # We aren't returning this to the user
    return response