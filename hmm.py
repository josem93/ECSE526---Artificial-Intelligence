from math import pow, factorial, exp;

# Class for generating Hidden Markov Model
class HMM(object):
	
	#lamda = 0.01;
	
	def __init__(self, vocab, unigram, bigram, trigram):
		self.words = vocab;
		self.unigram = unigram;
		self.bigram = bigram;
		self.trigram = trigram;
		self.wordSize = len(self.words);
		self.lamda = 0.01;
		self.iter = 0;
	
	
	# Function to run the sentence correction process
	def correctSentence(self, hmm, noisySentence):
		print('Starting Correction...');
		print();
		noisyWords = noisySentence.split();
		correctWords = [];
		tmp = self.words[10639];
		distanceTotal = 0;
		
		for i in range(len(noisyWords)):
			if(i == 0):
				x0 = noisyWords[i];
				correctWords.append(x0);
				distanceTotal += 0;
				self.iter += 1;
				
			else:
				if(hmm == 1 or self.iter == 1):
					message = ['Noisy Word:', noisyWords[i]];
					print(' '.join(message));
					print('Possible Words:');
					
					#get sample of possible words based on bigram
					key = self.stringToNum(correctWords[-1:]);
					sample = self.getSample(key);
					
					# if bigram samples do not contain noisy word in 2nd column then set correct word to noisy
					if(noisyWords[i] == tmp):
						k = self.levenshtein(tmp, noisyWords[i])
						correctWord = tmp;
						
						#add word to list of correct words
						correctWords.append(correctWord);

						# Annotated Output
						message1 = ['Word:', tmp, ' --> ', 'Edit Distance:', str(k), ',', 'Probability:', str(0.0)];
						print(' '.join(message1));
						message2 = ['Noisy Word: ', noisyWords[i], ' --> Correct Word: ', correctWord];
						print(' '.join(message2));
						print();
						continue;
					
					#get get conditional probability of Xt given Et
					Pxt_et = [];
					editDistances = [];
					m = 10000;
					minIndex = 0;
					for w in range(len(sample)):
						wordIndex = sample[w][1];
						#get edit distance
						k = self.levenshtein(noisyWords[i],self.words[wordIndex-1]);					
						if(k < m):
							m = k;
							minIndex = w;
						editDistances.append(k);	
					
					
					minDistances = [];
					secondToMinDistances = [];
					for	w in range(len(sample)):
						if(editDistances[w] == m):
							minDistances.append(sample[w]);
						if(editDistances[w] == m+1):
							secondToMinDistances.append(sample[w]);
					
					
					# check each word with the min edit distance
					Pxt_et0 = [];
					k = min(editDistances);
					Pet_xt = (pow(self.lamda,k)*exp(self.lamda))/factorial(k);
					for w in range(len(minDistances)):
						Pxt = minDistances[w][2];
						p = Pet_xt*Pxt;
						Pxt_et0.append(p);

					
					mi0 = 0;
					m0 = 0;
					for w in range(len(Pxt_et0)):
						if(Pxt_et0[w] > m0):
							m0 = Pxt_et0[w];
							mi0 = w;
					
					#Checks the next min edit distance words
					Pxt_et1 = [];
					k = min(editDistances)+1;
					Pet_xt = (pow(self.lamda,k)*exp(self.lamda))/factorial(k);
					for w in range(len(secondToMinDistances)):
						Pxt = secondToMinDistances[w][2];
						p = Pet_xt*Pxt;
						Pxt_et1.append(p);
					
					mi1 = 0;
					m1 = 0;
					for w in range(len(Pxt_et1)):
						if(Pxt_et1[w] > m1):
							m1 = Pxt_et1[w];
							mi1 = w;
					
					
					self.output(hmm, minDistances, min(editDistances), Pxt_et0);
					self.output(hmm, secondToMinDistances, min(editDistances), Pxt_et1);
					
					#get correct word
					if(m0 >= m1):
						for w in range(len(minDistances)):
							if(w == mi0):
								correctWord = self.words[minDistances[w][1]-1];
					else:
						for w in range(len(secondToMinDistances)):
							if(w == mi1):
								correctWord = self.words[secondToMinDistances[w][1]-1];
					
					
					#add word to list of correct words
					correctWords.append(correctWord);

					# Annotated Output
					message = ['Noisy Word: ', noisyWords[i], ' --> Correct Word: ', correctWord];
					print(' '.join(message));
					print();
					self.iter += 1;
					
				"""elif(hmm == 2):		# for a second order HMM
					#get sample of possible words based on bigram
					key = self.stringToNum(correctWords[-2:]);
					sample = self.getSample(key);
					
					# if bigram samples do not contain noisy word in 2nd column then set correct word to noisy
					if(noisyWords[i] == tmp):
						k = self.levenshtein(tmp, noisyWords[i])
						correctWord = tmp;
						
						#add word to list of correct words
						correctWords.append(correctWord);

						# Annotated Output
						message1 = ['Word:', tmp, ' --> ', 'Edit Distance:', str(k), ',', 'Probability:', str(0.0)];
						print(' '.join(message1));
						message2 = ['Noisy Word: ', noisyWords[i], ' --> Correct Word: ', correctWord];
						print(' '.join(message2));
						print();
						continue;
					
					#get get conditional probability of Xt given Et
					Pxt_et = [];
					editDistances = [];
					m = 10000;
					minIndex = 0;
					for w in range(len(sample)):
						wordIndex = sample[w][2];
						#get edit distance
						k = self.levenshtein(noisyWords[i],self.words[wordIndex-1]);					
						if(k < m):
							m = k;
							minIndex = w;
						editDistances.append(k);	
					
					
					minDistances = [];
					secondToMinDistances = [];
					for	w in range(len(sample)):
						if(editDistances[w] == m):
							minDistances.append(sample[w]);
						if(editDistances[w] == m+1):
							secondToMinDistances.append(sample[w]);
					
					
					# check each word with the min edit distance
					Pxt_et0 = [];
					k = min(editDistances);
					Pet_xt = (pow(self.lamda,k)*exp(self.lamda))/factorial(k);
					for w in range(len(minDistances)):
						Pxt = minDistances[w][3];
						p = Pet_xt*Pxt;
						Pxt_et0.append(p);
					#print(Pxt_et0);
					
					mi0 = 0;
					m0 = 0;
					for w in range(len(Pxt_et0)):
						if(Pxt_et0[w] > m0):
							m0 = Pxt_et0[w];
							mi0 = w;
					#print(mi0);
					
					#Checks the next min edit distance words
					Pxt_et1 = [];
					k = min(editDistances)+1;
					Pet_xt = (pow(self.lamda,k)*exp(self.lamda))/factorial(k);
					for w in range(len(secondToMinDistances)):
						Pxt = secondToMinDistances[w][3];
						p = Pet_xt*Pxt;
						Pxt_et1.append(p);
					#print(Pxt_et1);
					
					mi1 = 0;
					m1 = 0;
					for w in range(len(Pxt_et1)):
						if(Pxt_et1[w] > m1):
							m1 = Pxt_et1[w];
							mi1 = w;
					#print(mi1);
					
					
					self.output(hmm, minDistances, min(editDistances), Pxt_et0);
					self.output(hmm, secondToMinDistances, min(editDistances), Pxt_et1);
					
					#get correct word
					if(m0 >= m1):
						for w in range(len(minDistances)):
							if(w == mi0):
								correctWord = self.words[minDistances[w][2]-1];
					else:
						for w in range(len(secondToMinDistances)):
							if(w == mi1):
								correctWord = self.words[secondToMinDistances[w][2]-1];
					
					
					#add word to list of correct words
					correctWords.append(correctWord);

					# Annotated Output
					message = ['Noisy Word: ', noisyWords[i], ' --> Correct Word: ', correctWord];
					print(' '.join(message));
					print();
					self.iter += 1;"""
				
		# Annotated Output
		print('Corrected Sentence:');
		print(' '.join(correctWords));
		print();
		print('Correction Done...');
	
	
	# Function to display the annotated output of each possible word
	def output(self, hmm, distances, d, probs):
		if(hmm == 1 or self.iter == 1):
			for i in range(len(distances)):
				wordIndex = distances[i][1];
				word = self.words[wordIndex-1];			
				message = ['Word:', word, ' --> ', 'Edit Distance:', str(d), ',', 'Probability:', str(probs[i])];
				print(' '.join(message));
		"""elif(hmm == 2):
			for i in range(len(distances)):
				wordIndex = distances[i][2];
				word = self.words[wordIndex-1];			
				message = ['Word:', word, ' --> ', 'Edit Distance:', str(d), ',', 'Probability:', str(probs[i])];
				print(' '.join(message));"""
	
	
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
	
	
	# Function to get the key number(s) from the word string(s)
	def stringToNum(self, strings):
		key = [];
		for i in range(len(strings)):
			for w in range(self.wordSize):
				if(strings[i] == self.words[w]):
					key.append(w);
					break;
		
		return key;
		
	
	#Dynamic Programming algorithm to compute the Levenshtein distance between two strings
	#Obtained from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
	def levenshtein(self, s1, s2):
		if len(s1) < len(s2):
			return self.levenshtein(s2, s1);

		# len(s1) >= len(s2)
		if len(s2) == 0:
			return len(s1);

		previous_row = range(len(s2) + 1);
		for i, c1 in enumerate(s1):
			current_row = [i + 1];
			for j, c2 in enumerate(s2):
				insertions = previous_row[j + 1] + 1; # j+1 instead of j since previous_row and current_row are one character longer
				deletions = current_row[j] + 1;       # than s2
				substitutions = previous_row[j] + (c1 != c2);
				current_row.append(min(insertions, deletions, substitutions));
			previous_row = current_row;
		
		return previous_row[-1];