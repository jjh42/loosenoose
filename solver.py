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
        self._guess()

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

    def _guess(self):
        """Iterate through all the matches to find the distribution of letters."""
        letter_predictions = {}
        # Count the number of words each letter occurs in
        currentletters = set(self.word)
        for w in self.matching_words:
            # Ignore occurences of known letters
            letters = set(w); letters.difference_update(currentletters)
            for l in letters:
                try:
                    letter_predictions[l] += 1
                except KeyError:
                    letter_predictions[l] = 1
        # Turn the prediction dictionary into an ordered list from
        # most likley to least like.
        self.predictions = letter_predictions.items()
        self.predictions.sort(cmp=lambda x,y: -cmp(x[1], y[1]))
        # self.predictions is now an ordered list of tuples from most to least likely.
        # ('letter', number).
        # Normalize number of occurences to a fraction.
        self.predictions = map(lambda x: (x[0], float(x[1]/len(self.matching_words))),
                                          self.predictions)
