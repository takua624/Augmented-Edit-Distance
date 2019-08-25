from itertools import permutations

# Created by Yun-Fei "Takua" Liu

def repeat_score(w1,w2,cc):
	# default: w1 has more cc than w2
	NN = len(w1)
	cc_in_w1 = w1.count(cc)
	cc_in_w2 = w2.count(cc)
	if cc_in_w2 > cc_in_w1:
		tmp=w1
		w1=w2
		w2=tmp
	score = []
	# the position in w1 and w2 where cc occurs
	# for example, if w1 is "apple", and cc is "p",
	# then pos1 = [1,2], remember the index of Python begins from 0!
	pos1 = [ii for ii in range(NN) if w1[ii]==cc]
	pos2 = [ii for ii in range(NN) if w2[ii]==cc]
	
	# find the minimum sum of distances of all occurrences of cc in w1 and in w2
	# for example, w1="accc", w2="cbbc", cc="c"
	# pos1=[1,2,3], pos2=[0,3]
	# perm_pos1 = [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
	# because there are only 2 c's in w2, for each permutation in perm_pos1,
	# we only take the first 2 value to minus the corresponding value in pos2
	# in this case, the resulting possible scores are:
	# [1+1, 1+0, 2+2, 2+0, 3+2, 3+1]
	# the best case is 1+0, definitely. 
	# So in this case, the optimum mapping between the multiple c's is:
	# c1 in w1 maps to c0 in w2, and c3 in w1 maps to c3 in w2
	# c2 in w1 will lead to a penalty of extra repeated cc, which is handled not in this function, but in the calling function "same_length()"
	perm_pos1 = list(permutations(pos1))
	for perm in perm_pos1:
		pos1 = perm
		shorter = min(len(pos1), len(pos2))
		
		this_perm = 0
		for ii in range(shorter):
			this_perm += abs(pos1[ii]-pos2[ii])
		score += [this_perm]
	
	score = min(score)
		
	return score
			
def same_length(w1, w2, dynamic_repeat_penalty=True):
	NN = len(w1)
	score = 0
	for cc in sorted(list(set(w1))):
		cc_in_w1 = w1.count(cc)
		cc_in_w2 = w2.count(cc)
		# if a letter cc exists in w1 but not in w2,
		# add a penalty of [occurrences of cc in w1]*[length of word]
		if cc_in_w2==0:
			score += cc_in_w1*NN
			continue
			
		repeat_ratio = min(cc_in_w2/cc_in_w1, cc_in_w1/cc_in_w2)*dynamic_repeat_penalty
		repeat_ratio = repeat_ratio**1
		repeat_diff = cc_in_w1-cc_in_w2
		if cc_in_w1>cc_in_w2:
			score += repeat_diff*NN*(1-repeat_ratio)
		if cc_in_w1<cc_in_w2: # repeat_diff is a negative value in this case!
			score += repeat_diff*NN*(repeat_ratio)
			# this looks asymmetric, but it should be! 
			# because we are running this for loop with set(w1)
			# maybe we can adjust the penalty for letter number mismatch?
			# as long as two words share the same letter, the penalty shouldn't be as high as NN
			# what about dynamic penalty? the penalty drops as cc_in_w2/cc_in_w1 increases --> account for the fact that we don't care the number of "a" if the sequences are "aaaaaaaaa" and "aaaaaaaa"
			# when cc_in_w1<cc_in_w2, the score will be over-penalized by NN*(cc_in_w2-cc_in_w1) due to some letters the letter that corresponds to the extra cc's in w2. We have to subtract the extra penalty to achieve symmetry
		
		score += repeat_score(w2,w1,cc)
	return score
	
def augmented_ED(w1,w2, normalize=1, dynamic_repeat_penalty=True):
	if normalize not in [0,1,2]:
		normalize = 0
	# default: w1 longer than w2
	NN = max(len(w1),len(w2))
	if len(w2)==len(w1):
		return same_length(w1,w2, dynamic_repeat_penalty)/NN**normalize
	if len(w2)>len(w1):
		tmp=w1
		w1=w2
		w2=tmp
	len_diff = len(w1)-len(w2)
	score = NN**2
	# if w1 and w2 differ in length, pad the shorter one
	# find the scores for all possible padding, and pick the min score
	# for example, w1="cat", w2="scath",
	# possible padding: cat__, _cat_, __cat; _cat_ no doubt yields the min
	# "saturday" vs "day" should be more similar than "saturday" vs "say"
	# edit distance can't make this distinction!
	for ii in range(len_diff+1):
		w2_pad = "_"*ii+w2+"_"*(len_diff-ii)
		tmp_score = same_length(w1, w2_pad, dynamic_repeat_penalty)
		if tmp_score < score:
			score = tmp_score
	return score/NN**normalize

