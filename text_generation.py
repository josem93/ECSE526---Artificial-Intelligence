# File which runs the text generation process

import markov
from math import pow


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



markov = markov.MarkovModel(vocab, unigram, bigram, trigram);

markov.generateText();


"""###TESTS
def stringToNum(strings):
	key = [];
	for i in range(len(strings)):
		for w in range(len(vocab)):
			if(strings[i] == vocab[w]):
				key.append(w);
				break;
	
	return key;
	

	
#genWords = ['The', 'only'];
#key = stringToNum(genWords[-2:]);
genWords = ['<s>'];
key = stringToNum(genWords);
#print(key);

# get sample
list = [];
order = len(key);
if(order == 2):
	for i in range(len(trigram)):
		if(key[0]+1 == trigram[i][0] and key[1]+1 == trigram[i][1]):
			list.append(trigram[i]);
		
elif(order == 1):
	for i in range(len(bigram)):
		if(key[0]+1 == bigram[i][0]):
			list.append(bigram[i]);
elif(order == 0):
	list = unigram;
		
#print(list);
print(len(list));

	
def getProb(possibleWord, order=2):
	if(order == 2):
		return possibleWord[3];
		
	elif(order == 1):
		for i in range(len(bigram)):
			if(possibleWord[1] == int(bigram[i][0]) and possibleWord[2] == int(bigram[i][1])):
				return bigram[i][2];
				

# get Sps				
order = len(list[0])-2;
s = [x[len(list[0])-1] for x in list];

# use trigram and bigram distributions to get Sps
if(order == 2):	#trigram
	Sps = [];
	for i in range(len(list)):
		# create PD using a Gaussian Distribution
		Po1 = getProb(list[i], order);
		Po2 = getProb(list[i], order-1);
		Sps.append(Po1*Po2);
		
elif(order == 1):	#bigram
	Sps = s;
elif(order == 0):
	Sps = s;

#print(Sps);
#norm_Sps = normalize(Sps);
maxProb = max(Sps);
randomVar = maxProb+1;
while(randomVar > maxProb or randomVar < 0):
	randomVar = random.gauss(maxProb, maxProb);

print('Random Variable');	
print(randomVar);	
print('----');
	
#print(norm_Sps)
#sampleIndex = random.randint(0, len(list));
m = 1;
sampleIndex = 0;
for i in range(len(Sps)):
	#print('Distance');
	#print(abs(Sps[i]-randomVar));
	#print('m');
	#print(m);
	#print(abs(Sps[i]-randomVar) < m);
	if(abs(Sps[i]-randomVar) < m):
		sampleIndex = i;
		m = abs(Sps[i]-randomVar);
		#print('new min');


print(sampleIndex);
wordIndex = list[sampleIndex][order];
print(wordIndex);
newWord = vocab[wordIndex-1];

genWords.append(newWord);
print(' '.join(genWords));"""