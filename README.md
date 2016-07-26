# README

## PartI and PartII Overview

### Overview
NGrams builds language models for the training file. The language model includs unigram without smooth, bigram without smooth, trigram without smooth, interpolated bigram and interpolated trigram. Ngrams will caculate the perplexity of the whole test file instead of by sentence

### Files

1. Ngrams.py: the main class for building ngram language model
2. TextProcessor: the usage class to convert a plait text file to the text format that the Ngrams.py recognize.
3. trainfile_2.txt : training data for the toy problem
4. devfile_2.txt: development data for the toy problem
5. testfile_2.txt: test data for the toy problem
6. trainfile_4.txt: training data example
7. testfile_4.txt: test data example
6. README file


### Traininig and Testing Data
For generally usage, Ngrams could take general .txt file as its training or testing data as long as all the data is in the recognizable format.

For specific example, we provide a toy problem in the package(the trainfile of the toy problem is different from the posted one. If you are using the posted one, please preprocess it with textProcessor.py).
	Training: trainfile_2.txt
	Development file: devfile_2.txt
	Tesing file: testfile_2.txt

The training file is not in the recoginizable format. It is necessary to use the preprocess tool, which is also provided in the package, to convert it. 


### Program Description

#### Standard input and output:
	Input: trainingdata.txt devdata.txt test.txt
	Ouput: perpexity of test.txt

#### System requirement and Compile information
You will need at least python 2.7 to run the NGrams.py. You will need a bash shell or any other terminal to excute the program.
No need to compile. 
	

#### Excute
Under the directory that the NGrams.py located, please enter the following command in your shell:

	python Ngrams.py n trainfile.txt devfile.txt testfile.txt
	
	n: 1 -- unigram; 2 -- bigram; 3 -- trigram; 2s -- interpolated bigram; 3 -- interpolated trigram
	
For the toy problem, please enter the following command

	python Ngrams.py 2 trainfile_2.txt devfile_2.txt testfile_2.txt
		

#### Preprocess the text
The standard text form that NGram takes is as the following format:
`<s> sentence </s>`
`<s> sentence </s>`
......

#### Understand the printing results
The printing results includs:
Unigram Probability displayed as a dictionary:
Bigram Probabilty displayed as a dictionary:
Trigram Probability displayed as a dictionary:
lambda values if using interpolation model""
Perplexity of the whole file:


### Program machanism and function

#### 'UNK' threshold 
The UNK threshold is determined by the development file. The initial threshold is set as 2. However, it may change according to the performance of the development set.

#### Lambdas for interpolation model
The lambdas for interpolation model are determined by a simple hill climbing algorithm. Also , the performance development set will determine the best lambdas for the model.

### Potential bugs
1. NGrams.py may have error if the input files are not in the recognizable format. It is very important to make the  input file format be consistent with the standard format.
2. It is crucial to have certain amount of training data. Small data may make the perplexity run into inifinity(or 0) very easily. When the perplexity run very low, NGrams will return the perlexity as 0.
3. The program does not use type of words but simple tokenize of words.

## PARTIII

### Overview
At this part, we will develope languages models by using the SIRLM Ngram builder. The training and test data are from the MSR_DATA_CHALLENGE. The goal of this part is to test the performance of different ngrams models.

### Training data
The training data is from Project Gutenberg. To enhance the model accuracy, the trained models used not only single text file but 20 text files. 

### Models and files 
Langage models: I am using SIRLM toolkits to development the langage models for the training data. The models include unigram with laplace, bigram with laplace, trigram with laplace, trigram with laplace, interpolated bigram and interplated trigram.

Files: 

1. sirlmProcessor.py: To convert the text file into the recognizalbe format that the SIRLM toolkits takes
2. perplexity resluts of each sentences for each language model
3. the best answer results for each of the question model
4. The experiment report 
 

### Text Processing
In order to use the SIRLM toolkits, the training data has to been in recognizable format. A text processing program has been included in the pacakge -- sirlmProcessor. This program will take a standard .txt file as input. And the converted text file will be output to `output.txt`. 

The following command to run sirlmProcessor.py:
	
	python sirlmProcessor.py file.txt

How the sirlmProcessing processes the text:

1. Reading text by sentence and splitting the sentences: The sentence boundary is based on the punctuations, including: ".",";","?","!"
2. Cleaning the white space tokenize
3. Removing unnecessary numeric numbers such as the number tagged for each paragraph.


### Pipeline
As required, the scripts are not included in the package. However, in the pipeline, the program used several scripts to do batch processing. The following is the pipeline:

1. Read all the training text and then do text preprocess.
2. Train data by using SIRLM toolkits for each model and obtain the language model files, which is in .lm format
3. Test the Holmoes.IM_format.questions.txt on the language models and get the output.txt
4. Abtract the answers and perplexity for each sentences from the output.txt and format them into the recognizable format of the bestof5.pl
5. Use score.pl to caculate the performance from the output of bestof5.pl. 

Result Analysis and potential issues will be presented in the report.


 

