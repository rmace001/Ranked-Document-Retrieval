# ps2-Ranked-Document-Retrieval-rmace001
ps2-Ranked-Document-Retrieval created by GitHub Classroom
# Project Structure Description
An `InvertedIndex` class was built to store term-indices and document-length-indices from a subset of the ap89_collection documents. We perform ranked document retrieval along with implementing the following complexites: 
- Supports complex queries (using a phrase and not a single term)
- Utilizes the Vector Space Model and Cosine Similarity
- Utilizes word-stemming
- Removes stop-words from each query and document
- Evaluates various retrieval methods based on speed, precision, and recall
# `InvertedIndex` Class Description and Relevant Functions for Ranked Document Retrieval
- Class `InvertedIndex`
	- Data Members
		- set `stop_list_set`
		- list `term_list`
		- dict `term_index`
		- dict `doc_index`
	- Important Member Functions
		- `make_stop_list`
		- `make_term_list_and_doc_index`
		- `make_term_index`
		- `get_posting_list`
		- `get_q_weight`
		- `get_d_weight`
  - Other Important Functions
    - `cosine_score`
# Running InvertedIndex.py
To run this program, you must contain the files in the repository all in the same directory as this program. The files include an `ap89_collection` documents file and other necessary files that correspond to this program. From this point onward, you may now successfully run this python (version 3.0 and above) program. The `results_file.txt` contains the ranked retrieval scores for each query. The `output.txt` file contains the `trec_eval.pl` evaluation statistics.
# References
- CS172 L2-L3 Slides: Cosine Similarity Function
- https://www.youtube.com/watch?v=R-HLU9Fl5ug
- https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
- https://www.programiz.com/python-programming/methods/built-in/filter
- https://python-textbok.readthedocs.io/en/1.0/Classes.html#defining-and-using-a-class
- https://www.geeksforgeeks.org/python-string-split/
- https://pythonspot.com/tokenizing-words-and-sentences-with-nltk/
- https://www.dataquest.io/blog/web-scraping-tutorial-python/
