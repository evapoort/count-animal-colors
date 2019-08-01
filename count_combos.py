# -*- coding: utf-8 -*-
# jeroen.vanparidon@mpi.nl
import pandas as pd
import argparse
from utensils import log_timer
from collections import Counter


def create_combos(words_fname):
    """Creates a list of possible animal/color phrases to search for.

    :param words_fname: tab-separated file containing animals and colors to search for
    :returns: phrases to search for, colors to search for, and animals to search for
    """
    words = pd.read_csv(words_fname, sep='\t')
    animals = list(words['animal'].dropna())
    colors = list(words['color'].dropna())
    search_combos = dict()

    for animal in animals:
        plural = f'{animal}s' if not animal.endswith('y') else f'{animal[:-1]}ies'  # include plurals of type grizzly/grizzlies
        for color in colors:
            phrases = []
            phrases.append(f'{color} {animal}')
            phrases.append(f'{animal} {color}')
            phrases.append(f'{animal} s {color}')
            phrases.append(f'{animal} has {color}')
            phrases.append(f'{animal} is {color}')
            phrases.append(f'{animal} have {color}')
            phrases.append(f'{animal} are {color}')
            phrases.append(f'{color} {plural}')
            phrases.append(f'{plural} is {color}')
            phrases.append(f'{plural} has {color}')
            phrases.append(f'{plural} are {color}')
            phrases.append(f'{plural} have {color}')
            search_combos[(color, animal)] = phrases
    return search_combos, colors, animals


def pad(string):
    """String magic.

    Pads text string, replaces underscores with spaces
    replaces British spelling of gray with American spelling.
    This method generally makes the search phrases map correctly onto the corpus text.

    :param string: text string
    :returns: padded text string
    """
    string = string.strip('\n').replace('_', ' ').replace('grey', 'gray')
    return f' {string} '


@log_timer
def count_corpus(corpus_fname, words_fname):
    """Counts animal/color phrases in a text corpus.

    :param corpus_fname: text file containing corpus to search
    :param words_fname: tab-separated text file containing animals and words to search for
    :returns: Counter object containing counts
    """
    search_combos, colors, animals = create_combos(words_fname)  # get combos that we will be searching for

    combos = [f'{combo[0]} {combo[1]}' for combo in search_combos.keys()]
    combo_counts = Counter({x:0 for x in combos + animals + colors})  # start counter

    with open(corpus_fname, 'r') as corpus_file:  # open corpus file
        for line in corpus_file:  # go through corpus file line by line
            color_bool = False
            noun_bool = False
            line = pad(line.lower())

            for animal in animals:
                plural = f'{animal}s' if not animal.endswith('y') else f'{animal[:-1]}ies'
                if (pad(animal) in line) or (pad(plural) in line):
                    noun_bool = True
                    combo_counts.update([animal])

            # count colors
            for color in colors:
                if pad(color) in line:
                    color_bool = True
                    combo_counts.update([color])

            if color_bool and noun_bool:
                print(line)
                # count specific phrases
                for combo, phrases in search_combos.items():
                    for phrase in phrases:
                        if pad(phrase) in line:
                            combo_counts.update([f'{combo[0]} {combo[1]}'])

    return combo_counts


def counter_to_df(counter):
    """Method for dumping Counter object to pandas DataFrame

    :param counter: Counter object
    :returns: pandas DataFrame containing counts
    """
    df = pd.DataFrame.from_dict(counter, orient='index').reset_index().rename(columns={'index': 'combo', 0: 'count'})
    return df


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='count animal-descriptor phrases in a corpus')
    argparser.add_argument('corpus_fname', help='text corpus to search')
    args = argparser.parse_args()

    words_fname = 'animals_colors.tsv'
    combo_counts = count_corpus(args.corpus_fname, words_fname)
    results_fname = args.corpus_fname.split('/')[-1].replace('.txt', '.counts.tsv')
    counter_to_df(combo_counts).sort_values('count', ascending=False).to_csv(results_fname, sep='\t')
