#!/usr/bin/env python3

class Wordle:
    def __init__(self, word_limit = 5000):
        self.word_frequency = dict(record.strip().split("\t") for record in open("word_frequency.txt"))
        self.words = list(self.word_frequency.keys())[:word_limit]

        self.letter_counts = [{}, {}, {}, {}, {}]
        for word in self.words:
            for i in range(5):
                letter = word[i]
                counts = self.letter_counts[i]
                if letter not in counts:
                    counts[letter] = 0

                counts[letter] += 1

        self.letter_dists = [[], [], [], [], []]
        for counts, dist in zip(self.letter_counts, self.letter_dists):
            d = sorted(list(counts.items()), key = lambda item: -item[1])
            dist.extend(d)

        self.word_scores = dict((word, self.score(word)) for word in self.words)

        #self.print_best(self.words)
        self.not_letters = set()
        self.else_letters = set()
        self.not_letters_i = [set(), set(), set(), set(), set()]
        self.letters = [None, None, None, None, None]


    def score(self, word):
        from math import log
        mult = 1#log(int(self.word_frequency[word]))
        return sum(self.letter_counts[i].get(letter, 0) for i, letter in enumerate(word)) * len(set(word)) * mult

    def print_best(self, words):
        print("\n".join("%s %r" % e for e in self.best_words(words)))

    def best_words(self, words):
        return sorted(((word, self.word_scores[word]) for word in words), key=lambda item: item[1])

    def set_letter(self, letter, i):
        self.letters[i] = letter

    def not_letter(self, letter):
        self.not_letters.add(letter)

    def else_letter(self, letter, i):
        self.else_letters.add(letter)
        self.not_letters_i[i].add(letter)

    def apply(self, word, info):
        for i, letter, mark in zip(range(5), word, info):
            if mark == 'y':
                self.set_letter(letter, i)
            elif mark == 'n':
                self.not_letter(letter)
            elif mark == 'e':
                self.else_letter(letter, i)
            else:
                raise Exception()

    def filter(self):
        for word in self.words:
            cont = False
            # discard words without set letters
            for i, letter in enumerate(self.letters):
                if letter is not None:
                    if word[i] != letter:
                        cont = True
                        break

            if cont is True:
                continue


            # discard words with not_letters (without the currently set letter) or not_letters[i]
            cont = False
            for i, letter in enumerate(word):
                if letter in self.not_letters.difference(set([self.letters[i]])) or letter in self.not_letters_i[i]:
                    cont = True
                    break

            if cont is True:
                continue

            cont = False
            # discard words without else letters
            for letter in self.else_letters:
                if letter not in word:
                    cont = True
                    break

            if cont is True:
                continue

            yield word

    def print_best_filtered(self):
        self.print_best(self.filter())

def main():
    from sys import argv

    args = argv[1:]

    word_limit = int(args.pop(0))

    wordle = Wordle(word_limit)
    

    while len(args) >= 2:
        word = args.pop(0)
        info = args.pop(0)
        wordle.apply(word, info)


    wordle.print_best_filtered()



if __name__ == '__main__':
    main()
