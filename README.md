# Augmented-Edit-Distance
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
## Reference
[1] Coltheart, M., Davelaar, E., Jonasson, J. T., & Besner, D. (1977). Access to the Internal Lexicon.

[2] Barnhart, A. S., & Goldinger, S. D. (2015). Orthographic and phonological neighborhood effects in handwritten word perception.

[3] Burt, J. S., McFarlane, K. A., Kelly, S. J., Humphreys, M. S., Weatherall, K., & Burrell, R. G. (2017). Brand name confusion: Subjective and objective measures of orthographic similarity.

[4] Yarkoni, T., Balota, D., & Yap, M. (2008). Moving beyond Coltheart’s N: A new measure of orthographic similarity.

[5] Whitney, C. (2001). How the brain encodes the order of letters in a printed word: The SERIOL model and selective literature review.

[6] Davis, C. J. (2001). The self-organising lexical acquisition and recognition (SOLAR) model of visual word recognition.
