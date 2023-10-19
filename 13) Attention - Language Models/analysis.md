# Analysis

## Layer 4, Head 6

This attention head seems to focus on the relationship between each word and the one that comes before. When analyzing the diagrams, we can recognize a consistent patter where each word has higher attension scores with the immediate antecedent word.

Example Sentences:
- I ate the [MASK], and I really liked it.
    For example, for the word "ate", the attention score was highest on "I"; for the word "the", the attention score was highest on "ate"; and so on and so forth.
- The dog chased the [MASK] around the house.
    For example, for the word "dog", the attention score was highest on "the"; for the word "the", the attention score was highest on "chased"; and so on and so forth.

## Layer 9, Head 12

This attention head seems to focus on the relationship between the MASK and the verb of which the mask is the object. When analyzing the diagrams, we can recognize a consistent patter where the MASK has higher attension scores close to its verb. However, this pattern seems to be consistent only when the MASK is the object of a verb.

Example Sentences:
- I drink a [MASK] at the bar.
    For example, the highest attention score is recorded between the MASK and the word "drink".
- I sometimes buy [MASK] for my mom.
    The highest attention score is recorded between the MASK and the word "buy".

## Layer 6, Head 1

This attention head seems to focus on the relationship between the articles and their nouns. When analyzing the diagrams, we can recognize a consistent patter where each article has higher attension scores close to the noun it is reffering to.

Example Sentences:
- A dog and a cat [MASK] around the house.
    For example, both the first and the second "a" have a higher attention scores close to the nouns they are refering to "dog" and "cat"; moreover, the article "the" has a higher attention score on "house".
- The mom [MASK] for the daughter.
    Both articles have higher attention scores close to the nouns they are refering to "mom" and "daughter".