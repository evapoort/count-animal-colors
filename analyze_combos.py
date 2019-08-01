# -*- coding: utf-8 -*-
# jeroen.vanparidon@mpi.nl
import numpy as np
import pandas as pd
import argparse
from utensils import log_timer


@log_timer
def analyze_combos(combos_fname, words_fname, canonical_fname):
    """Analyze animal/color counts files.

    Adds boolean variables for type of entry (noun, adjective, or combination)
    and computes forward and backward transitional probabilities.

    :param combos_fname: pandas DataFrame containing counts
    :param words_fname: pandas DataFrame containing all animals and colors
    :param canonical_fname: pandas DataFrame containing typical color for each animal
    :returns: pandas DataFrame containing results
    """
    words = pd.read_csv(words_fname, sep='\t')  # read in words
    combos = pd.read_csv(combos_fname, sep='\t')  # read in combo counts
    canonical = pd.read_csv(canonical_fname, sep='\t')  # read in the canonical combinations

    # boolean trait variables
    combos['is combo'] = combos['combo'].apply(lambda x: True if len(x.split(' ')) == 2 else False)
    combos['is color combo'] = combos['combo'].apply(lambda x: True if len(x.split(' ')) == 2 and x.split(' ')[0] in words['color'].values else False)
    combos['is animal'] = combos['combo'].apply(lambda x: True if x in words['animal'].values else False)
    combos['is color'] = combos['combo'].apply(lambda x: True if x in words['color'].values else False)
    combos['is adjective'] = combos['combo'].apply(lambda x: True if (x in words['color'].values) else False)

    # drop irrelevant attributes
    combos = combos.loc[combos['is adjective'] | combos['is animal'] | combos['is color combo']].reset_index()

    # constituent words
    combos['adjective'] = combos.apply(lambda x: np.nan if x['is animal'] else x['combo'].split(' ')[0], axis=1)
    combos['animal'] = combos.apply(lambda x: np.nan if x['is adjective'] else x['combo'].split(' ')[-1], axis=1)

    # constituent word counts
    combos['adjective count'] = combos[['adjective']].merge(combos, how='left', left_on='adjective', right_on='combo')['count']
    combos['animal count'] = combos[['animal']].merge(combos, how='left', left_on='animal', right_on='combo')['count']

    # transitional probabilities
    combos['forward tp'] = combos['count'] / combos['adjective count']
    combos['backward tp'] = combos['count'] / combos['animal count']

    # canonical combo
    combos['canonical color'] = combos[['animal']].merge(canonical, how='left', left_on='animal', right_on='animal')['canonical color']
    combos['canonical color'] = combos.apply(lambda x: np.nan if x['is adjective'] else x['canonical color'] + ' ' + x['animal'] , axis=1)
    combos['canonical color count'] = combos.apply(lambda x: np.nan if x['is adjective'] else combos.loc[combos['combo'] == x['canonical color']]['count'].max(), axis=1)

    # most common combo (and count)
    combos['most common non-canonical color'] = combos.apply(lambda x: np.nan if x['is adjective'] else combos.iloc[combos.loc[(combos['animal'] == x['animal']) & combos['is color combo'] & (combos['combo'] != x['canonical color'])]['count'].idxmax()]['combo'], axis=1)
    combos['most common non-canonical color count'] = combos.apply(lambda x: np.nan if x['is adjective'] else combos.loc[(combos['animal'] == x['animal']) & combos['is color combo'] & (combos['combo'] != x['canonical color'])]['count'].max(), axis=1)

    return combos


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='analyze animal/color phrase counts and compute conditional probabilities')
    argparser.add_argument('counts_fname', help='tab separated file containing counts')
    args = argparser.parse_args()

    words_fname = 'animals_colors.tsv'
    canonical_fname = 'canonical_colors.tsv'

    combos = analyze_combos(args.counts_fname, words_fname, canonical_fname)
    combos.to_csv(args.counts_fname.replace('.counts.tsv', '.results.tsv'), sep='\t')
