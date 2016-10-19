from random import gauss

# Class for generating Markov Model
class MarkovModel(object):
	
	
	def __init__(self, vocab, unigram, bigram, trigram):
		self.words = vocab;
		self.unigram = unigram;
		self.bigram = bigram;
		self.trigram = trigram;
		self.wordSize = len(self.words);
		
		
	# Function to get the list of tuples from the probability counts that contain the given key.
	def getSample(self, key):
		list = [];
		order = len(key);
		if(order == 2):
			for i in range(len(self.trigram)):
				if(key[0]+1 == self.trigram[i][0] and key[1]+1 == self.trigram[i][1]):
					list.append(self.trigram[i]);
				
		elif(order == 1):
			for i in range(len(self.bigram)):
				if(int(key[0])+1 == int(self.bigram[i][0])):
					list.append(self.bigram[i]);
		elif(order == 0):
			list = unigram;
		
		return list;
	
	# Function to obtain the new word given a list of possible next words
	def getNewWord(self, sample):
		# get Sps
		order = len(sample[0])-2;
		p = [x[len(sample[0])-1] for x in sample];
		
		# use trigram and bigram distributions to get Sps
		if(order == 2):	#trigram
			Sps = [];
			for i in range(len(sample)):
				Po1 = self.getProb(sample[i], order);
				Po2 = self.getProb(sample[i], order-1);
				Sps.append(Po1*Po2);
				
		elif(order == 1):	#bigram
			Sps = p;
		elif(order == 0):
			Sps = p;
		
		# create distribution and randomly sample from it.
		maxProb = max(Sps);
		randomVar = maxProb+1;
		while(randomVar > maxProb or randomVar < 0):
			randomVar = gauss(maxProb, maxProb);

		
		#get value closest to random variable
		m = 1;
		sampleIndex = 0;
		for i in range(len(Sps)):
			if(abs(Sps[i]-randomVar) < m):
				sampleIndex = i;
				m = abs(Sps[i]-randomVar);
				#print('new min');
		
		wordIndex = int(sample[sampleIndex][order]);
		newWord = self.words[wordIndex-1];
		return newWord;
	
	
	# Function to get the conditional probabilities from the trigram and bigram given the order of the process
	def getProb(self, possibleWord, order=2):
		if(order == 2):
			return possibleWord[3];
			
		elif(order == 1):
			for i in range(len(self.bigram)):
				if(possibleWord[1] == int(self.bigram[i][0]) and possibleWord[2] == int(self.bigram[i][1])):
					return self.bigram[i][2];
					
		
	# Function to get the key number(s) from the word string(s)
	def stringToNum(self, strings):
		key = [];
		for i in range(len(strings)):
			for w in range(self.wordSize):
				if(strings[i] == self.words[w]):
					key.append(w);
					break;
		
		return key;
		
	
	# Function to run the text generation process
	def generateText(self):
		
		# Set x0 = <s> (153 in vocab.txt)
		x0 = self.words[152];
				
		# Initialize list to hold sentence
		genWords = [x0];
		numWords = 0;
		
		# Run loop until the the word "</s>" is obtained
		while 1:
			numWords += 1;
			print('Word #' + str(numWords));
			if(len(genWords) == 1):
				# get next word from bigram_counts
				key = self.stringToNum(genWords);
				sample = self.getSample(key);
				newWord = self.getNewWord(sample);
			
			if(len(genWords) > 1):
				# generate sample of (x(t-1), x(t-2))
				key = self.stringToNum(genWords[-2:]);		#list of word indices
				sample = self.getSample(key);
				
				if(len(sample) == 0):
					#print(' '.join(sum(['Backed-Off at ('], key, ')')))
					# backoff (set new key)
					key = key[1:];
					sample = self.getSample(key);
					newWord = self.getNewWord(sample);
					
				else:
					newWord = self.getNewWord(sample);
			
			# add new word to list of generated words
			print(newWord);
			genWords.append(newWord);
			
			# break when the new word is the sentence termination string </s>
			if(newWord == self.words[151]):
				break;
			
		print(' '.join(genWords));