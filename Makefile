.PHONY: all clean

all: word_frequency.txt

word_frequency.txt: count_1w100k.txt
	grep '^[A-Z][A-Z][A-Z][A-Z][A-Z][^A-Z]' count_1w100k.txt | tr 'A-Z' 'a-z' > word_frequency.txt

count_1w100k.txt:
	wget https://norvig.com/ngrams/count_1w100k.txt

clean:
	rm count_1w100k.txt word_frequency.txt
