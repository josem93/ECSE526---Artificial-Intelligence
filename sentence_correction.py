import hmm
from math import pow, factorial, exp;
l = 0.01;
vocabFile = "data/vocab.txt";
unigramFile = "data/unigram_counts.txt";
bigramFile = "data/bigram_counts.txt";
trigramFile = "data/trigram_counts.txt";

# Function to get all words from given file
def fileToWords(vocabFile):
	words = [];
	with open(vocabFile, "r") as fp:
		for i in list(fp):
			tmp = i.split();
			try:
				words.append(tmp[1]);
			except:pass
	
	return words;

# Function to get the probability data from unigram_counts data
def getUnigram(unigramFile):
	unigram = [];
	with open(unigramFile, "r") as fp:
		for i in list(fp):
			tmp = i.split();
			try:
				unigram.append(pow(10, float(tmp[1])));
			except:pass
	
	return unigram;
	
# Function to get the 1st order conditional data from bigram_counts data
def getBigram(bigramFile):
	bigram = [];
	with open(bigramFile, "r") as fp:
		for i in list(fp):
			tmp = i.split();
			try:
				bigram.append((int(tmp[0]), int(tmp[1]), pow(10,float(tmp[2]))));
			except:pass
	
	return bigram;

# Function to get the 2nd order conditional data from trigram_counts data
def getTrigram(trigramFile):
	trigram = [];
	with open(trigramFile, "r") as fp:
		for i in list(fp):
			tmp = i.split();
			try:
				trigram.append((int(tmp[0]), int(tmp[1]), int(tmp[2]), pow(10, float(tmp[3]))));
			except:pass
	
	return trigram;

	
vocab = fileToWords(vocabFile);				# Get all words from vocab.txt file
unigram = getUnigram(unigramFile);           # Get unigram probabilities from unigram.txt file
bigram = getBigram(bigramFile);              # Get bigram conditional probabilities from bigram.txt file
trigram = getTrigram(trigramFile);           # Get trigram conditional probabilities from trigram.txt file

s1 = '<s> I think hat twelve thousand pounds';
s2 = '<s> she haf heard them';
s3 = '<s> She was ulreedy quit live';
s4 = '<s> John Knightly wasn’t hard at work';
s5 = '<s> he said nit word by';

sentences = [s1,s2,s3,s4,s5];

hmmOrder = 1;

hmm = hmm.HMM(vocab, unigram, bigram, trigram);
#hmm.correctSentence(hmmOrder, s1);

# run in batch
for i in range(len(sentences)):
	hmm.correctSentence(hmmOrder, sentences[i]);
