# Augmented-Edit-Distance
## Description of the function
In the Python script `augmented_edit_distance.py`, you will find the function `augmented_ED()`.
It takes two words as input (`w1` and `w2`), and returns the "distance" between the words in terms of their spelling. 
Please note that conceptually, "distance" is the opposity of "similarity".
It takes three parameters:
* `normalize`: 0, 1, or 2. Default 1 
  - 0: the maximum "distance" between two words is the square of the length of the longer word. E.g., the distance between "STAR" and "BLUE" is 16, between "CAR" and "DOG" is's 9.
  - 1: the maximum "distance" between two words is the length of the longer word. E.g., the distance between "STAR" and "BLUE is 4, between "CAR" and "DOG" it's 3
  - 2: the "distance" falls between 0 and 1. E.g., the distance between "STAR" and "BLUE" and between "CAR" and "DOG" are both 1.
* `dynamic_repeat_penalty`: True or False, default True. Controls whether or not to regard two strings of repeated letters to be more similar when the ratio between the lengths of both strings approaches 1. E.g., if set to True, "aaaaaaaaa" and "aaaaaaaa" are considered more similar than "aaa" and "aa", although the strings in both pairs differ by 1 letter.
* `onset_weight`: from 0 to 1, default 0. Controls how important shared initial letter is to the similarity between words. When set to 0, shared initial letter is not taken into account. E.g., the distance between "abcd" and "axyz" and the distance between "abcd" and "xbyz" are both 3. When set to 1, two words are regarded as identical if they share the initial letter. That is, the distance between "abcd" and "axyz" is 0. If you'd like to use this feature, you may set it to no larger than 0.2.
## Background
Orthographic similarity measures how similar two words are spelled. It is intuitive that in terms of spelling, “CAT” is more similar to “CAR” than to “DOG”, but how similar is it? While “CAT” is also more similar to “ACT” than to “DOG”, between “ACT” and “CAR”, which one is more similar to “CAT”? An objective orthographic similarity metric seeks to quantify and distinguish between different levels of similarity.

An Orthographic similarity metric can be useful in both academic and practical settings. For example, in linguistics, it can be used to define the “orthographic neighborhood” of any given word. Coltheart et al. (1977) [1] defined the orthographic neighborhood of a given word to be all the words that can be derived from the target word by changing exactly one letter, while the positions of the other letters are preserved. For example, “CAR” is in the orthographic neighborhood of “CAT”, but neither “ACT” nor “DOG” is. Based on the knowledge of orthographical neighborhoods, psycholinguistic experiments can be designed to investigate the effect of neighborhood size, as opposed to word frequency and other properties of a word, on word recognition [2].

An orthographic similarity metric can also exhibit practical value beyond academics. For example, Burt et al. (2017) [3] suggested a possible use of orthographic similarity metrics in legal practice to determine the similarity between existing brand names a new brand name which seeks registration. 

Here, I propose a novel orthographical similarity metric which complements existing metrics and address the problems they faced. In brief, this novel orthographical similarity metric, the augmented edit distance (AED), yields symmetric results for any pair of words, normalized values comparable across word pairs, and fine-grained distinction between the similarity of a given word to different anagrams of another word.
## Levenshtein edit distance
Levenshtein edit distance was proposed by Yarkoni et al. (2008) [4], and is the most widely used orthographic similarity metric.

In brief, Levenshtein edit distance measures how many operations it takes to convert one word to another. An operation can be any of the following manipulations: the insertion of a letter, the deletion of a letter, and the replacement of one letter with another. For example, to convert the word “CAT” to the word “CAR”, we have to replace “T” with “R”, thus the edit distance between “CAT” and “CAR” is 1. Take the words “SUNDAY” and “SATURDAY” as another example, to convert “SUNDAY” to “SATURDAY”, we keep the “S”, insert “A” and “T”, replace “N” with “R”, and keep “D”, “A”, and “Y”. There are on replacement and two insertions, so the edit distance between “SUNDAY” and “SATURDAY” is 3.

Although Levenshtein edit distance is an elegant algorithm, it has some insufficiencies.

The main issue with Levenshtein edit distance is that it’s agnostic of letter positions. Because it only allows for insertion, deletion, and replacement, “swapping” two letters is considered two replacements, the same as replacing those letters with completely different ones. Therefore, in terms of Levenshtein edit distance, a word is as different from its own anagram as any other unrelated word. For example, the edit distance between “STAR” and “RATS” is 4, so is the distance between “STAR” and “BLUE”.

Additionally, because Levenshtein edit distance is agnostic of letter positions, a contiguous sub-string of a word is considered as similar to the word as a string made out of disconnected letters in the word. For example, both the edit distances between “DAY” and “SATURDAY” and between “TRY” and “SATURDAY” are 5.

Interested reader may varify these issues by running the Python implementation of Levenshtein edit distance included in this repository: `edit_distance.py`.
## Other distance measures and their drawbacks
Two other frequently cited distance measures are "open-bigram coding" [5] and "superposition matching" [6]. They are both ingenious algorithms; however, I will not go into the details of their implementations. The drawback of open-bigram coding is that, it is asymmetric. That is, the distance between word 1 and word 2 is different from that between word 2 and word 1. The superposition matching algorithm also yields asymmetric outputs when there are repeated letters in the input words. 

Davis programmed a “Match Calculator” which implemented both the superposition matching (named “SOLAR (Spatial Coding)”) and the open-bigram similarity metric (named “SERIOL_2001 (Open Bigram)”), and is freely available online (http://www.pc.rhul.ac.uk/staff/c.davis/Utilities/MatchCalc/index.htm), interested readers may explore the issues with these orthographic similarity metric mentioned in this section. (In all the examples concerning superposition matching in this article, the parameter “sigma” is 1, and “dynamic end letter marking” is disabled.)
## The augmented edit distance
To overcome the drawbacks of the three orthographic similarity metrics while retaining their advantages, I propose the augmented edit distance (AED).

The AED has five key features:
1. Shared letters between word1 and word2 are considered. Therefore, anagrams are considered more similar than totally unrelated words.
2. The output is symmetric, the distance between word1 and word2 is the same as the distance between word2 and word1.
3. It functions normally even when there are repeated letters in either word.
4. It accounts for the fact that humans are unable to distinguish the quantities of items in two arrays when the ratio between the quantities approaches 1.
5. It offers the option to regard words that share the same initial letters as more similar.

In the following sub-sections, I’ll introduce the working principles of AED.
### The vanilla case: same length, no repeated letter
To estimate the orthographic similarity between word 1 and word 2, the AED algorithm basically calculates for each letter in word 1 the (absolute) difference between its positions in both words. If a letter exists only in word 1, the “difference” is the length of word 1, which indicates this letter can’t be found in word 2. These differences are summed together and divided by the length of word 1, the resulting value is the augmented edit distance between word 1 and word 2.

If word 1 and word 2 use completely different set of letters, there AED value is the length of word 1, which is the maximum distance between word 1 and any word with the same length. In this aspect, AED is similar to Levenshtein edit distance.

The following table illustrates how to derive the AED values between “STAR” and “RATS”, and between “STAR” and “BLUE”.
![image](https://user-images.githubusercontent.com/26756686/202929460-4566c695-d3d3-4b7f-ad87-1f294dad411f.png)

### Same length, with repeated letters
Suppose there is a shared repeated letter C between word 1 and word 2. C repeats N times in word 1, and M times in word 2, denoted [C11, C12, … C1N] and [C21, C22, … C2M], respectively. Suppose N>M. The AED algorithm treats all M C’s as different letters and all N C’s as different letters, and among the N C’s in word 1, M of them are the same as the M C’s in word 2, the job of the AED algorithm is to find the optimum pairing between M C’s in word 1 and M C’s in word 2 that results in the smallest distance.

To do so, the AED algorithm generates all the possible pairings between the C’s in word 1 and the C’s in word 2. The number of all possible pairings is:
![image](https://user-images.githubusercontent.com/26756686/202929525-f68e62d2-d86b-41e3-8fa9-f8ee7726f3d3.png)

For each pairing, such as [(C11, C21), (C12, C22),…..., (C1M, C2M), C1(M+1), ……, C1N], the distances between the C pairs is calculated and summed. Each of the (M-N) C’s which isn’t paired with a C in word 2 is regarded as a letter that exist only in word 1, and is attributed the length of word 1 as its distance. The minimum sum of distances among all pairings is selected as the overall distance of the repeated letter C, and summed together with the distances of the unique letters. If there are multiple different repeated letters in the words, the minimum sum of distances for each repeated letter is computed.

The following table illustrates the computation for the AED value between “XAAAY” and “ABCAD”. Note that the “A”s that are paired up are persented in the same color.

![image](https://user-images.githubusercontent.com/26756686/202929581-55083a74-3803-4792-902e-e2cfb3b6e30f.png)
### Words with different lengths
If the two words to compare are different in length, the shorter word is padded with non-alphabetical symbols such as “\_” to attain the identical length as the longer word.
### Strings of repeated letters with different length
When we compare the numbers of identical dots in two arrays, we are keen to notice the ratio between the numbers, but not the absolute difference between them. For example, while we can tell the difference between 2 dots and 3 dots, it may be very hard to tell the difference between 100 dots and 101 dots. This is the Weber's Law (https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law). 

Likewise, a string pair like "aaaaaaaaaa" and "aaaaaaaaa" should be more difficult to tell apart from a pair like "aaa" and "aa" - although they both have the distance of 1. 

In AED, when the same letter appears multiple times in either word, the computed distance between the two words is reduced according to the ratio between the numbers of appearance. You can turn on and off this functionality by setting the parameter `dynamic_repeat_penalty` to True or False.
### Words that begin with the same letter
We perceive a pair words that begins with the same letter to be more similar than a pair of words with different initial letters. You may decide how important the shared initial letter should be by passing a value (between 0 and 1) to the parameter `onset_weight`.

### Normalization
In terms of the raw output (`normalize = 0`), the maximum "distance" between two words is the square of the length of the longer word. For example, the "distance" between "STAR" and "BLUE" is 16. If `normalize = 1`, the raw output is divided by the length of the longer word, such that the maximum distance is the length of the longer word - which is in the same scope as Levenshtein edit distance. If you want to compare the output of AED and the output of Levenshtein edit distance, please set `normalize` to 1. If `normalize = 2`, the raw output is devided by the square of the length of the longer word, such that the output falls between 0 and 1.
## Author
This function is designed by Yun-Fei "Takua" Liu.
https://yunfeitakualiu.com/
## Reference
[1] Coltheart, M., Davelaar, E., Jonasson, J. T., & Besner, D. (1977). Access to the Internal Lexicon.

[2] Barnhart, A. S., & Goldinger, S. D. (2015). Orthographic and phonological neighborhood effects in handwritten word perception.

[3] Burt, J. S., McFarlane, K. A., Kelly, S. J., Humphreys, M. S., Weatherall, K., & Burrell, R. G. (2017). Brand name confusion: Subjective and objective measures of orthographic similarity.

[4] Yarkoni, T., Balota, D., & Yap, M. (2008). Moving beyond Coltheart’s N: A new measure of orthographic similarity.

[5] Whitney, C. (2001). How the brain encodes the order of letters in a printed word: The SERIOL model and selective literature review.

[6] Davis, C. J. (2001). The self-organising lexical acquisition and recognition (SOLAR) model of visual word recognition.
