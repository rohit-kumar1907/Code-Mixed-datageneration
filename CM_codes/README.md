Code-Mixed Data Generation

### Preprocessing:
1. Cleaning the data to remove unnecessary discrepancies in cases where Sentence
Alignment was not there. we remove the ne word sentences.

2. Chunking the cleaned parallel corpora. English data is chunked using Stanford constituency parser, while the Hindi data is chunked using Shallow parser by LTRC, IIIT Hyderabad.

3. Word Alignment extraction using Giza++ for the parallel corpus. tool is run on both way keeping English as base and at the other time Hindi as Base.
Moreover we arranged the translation in the decreasing probability sequence.

4. Head finding, output of LTRC Parser contained the head of each chunk.We extracted them. But this was not the case in Stanford Parser’s output. We used a list of possible tags that can act as a head, and used this list to find head of each chunk.

## Sentence Generation:

1. We first extracted following information from the respective chunks of Hindi ad English such as the list oh heads, tags associated wiith heads, phrases i.e. head and words associated with them as tails, and pos tags associated with these phrases.

2. we replaced maximum 3 NPs in Hindi sentences with corresponding English NPs. 
for each Nps of hindi sentence we find all its corresponding word match in english from Giza++ output file and append in the variable 'match'. 

3. after that now for each NPs of english sentences we check whether that word is present in the list 'match', if it's present in the list we returned the position of phrase corresponding to that head of english word and replace it in the hindi sentences.

4. Thus we get our Code-mixed Hindi-English sentences, Hindi as base.

*issue:* 
1. Redundancy of Postposition/Preposition
2. Redundancy of words due to difference in number of chunks
