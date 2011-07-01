import gzip
import pickle
import re

class InvalidWordException(Exception):
    pass

class Dictionary():
    """This class does most of the hard work. Given a partial match it loads the dictionary, sorts it, etc."""
    def __init__(self, word):
        """Loads the dictionary of words of the correct length and matches."""
        self.word = self._preprocess(word)
        self._load_dict()
        self._match_words()

    def _preprocess(self, word):
        """Return the word in standard, canonical form."""
        word = word.lower()
        # Check word only contains alphabetical characters and ?
        for l in word:
            if l != '?' and (not l.isalpha()):
                raise InvalidWordException()
        return word
    
    def _load_dict(self):
        """Load the word dictionary of the correct length."""
        word_len = len(self.word)
        filename = 'words/words-%d.gz' % word_len
        f = gzip.open(filename, 'r')
        self.word_list = pickle.load(f)
        f.close()

    def _match_words(self):
        """Iterate through the word list and find any words that match."""
        existing_letters = set(self.word); existing_letters.discard('?');
        not_existing_letters = '[^' + ''.join(existing_letters) + ']'
        reobj = re.compile(self.word.replace('?', not_existing_letters))
        self.matching_words = filter(lambda s: reobj.match(s) != None, self.word_list)

