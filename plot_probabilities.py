import numpy as np
import pandas as pd
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
mpl.use('agg')
plt.style.use('seaborn')
font_scale = .6
font_size = 10 * font_scale
sns.set(context='paper', style='whitegrid', palette='Set2', font_scale=font_scale)

def plot_probabilities(df, label):
    g = sns.catplot(y='animal', x='conditional probability', hue='condition',
                    kind='bar', data=df,
                    height=len(df) / 12, aspect=1 / np.log10(len(df)))
    g.set(xscale='log', ylabel='', xlim=(1e-5, 1))
    g._legend.set_title('')
    g._legend.texts[0].set_text(f'canonical {label}')
    g._legend.texts[1].set_text(f'most common\nother {label}')
    for i, row in df.iterrows():
        if i % 2 == 1:
            va = 'top'
            ypos = (i / 2) - .5
        else:
            va = 'bottom'
            ypos = i / 2
        if row['conditional probability'] > 0:
            xpos = row['conditional probability']
            color = 'black'
        else:
            xpos = 1e-5
            color = 'gray'
        g.ax.text(xpos, ypos, ' ' + row['adjective'], fontsize=font_size * .7, va=va, color=color)
    return g

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='plot conditional probabilities from corpus analysis')
    argparser.add_argument('results_fname')
    args = argparser.parse_args()

    df = pd.read_csv(args.results_fname, sep='\t')
    df = df.loc[df['is animal']]
    df_color = pd.melt(df,
                       id_vars=['animal', 'count', 'canonical color count', 'most common non-canonical color count'],
                       value_vars=['canonical color', 'most common non-canonical color'],
                       var_name='condition',
                       value_name='color')
    df_color['adjective'] = df_color['color'].apply(lambda x: x.split(' ')[0])
    df_color['conditional probability'] = df_color.apply(lambda x: x[x['condition'] + ' count'] / x['count'], axis=1)
    df_color['sort'] = df_color['most common non-canonical color count'] / df_color['count']

    plt.clf()
    plot_probabilities(df_color.sort_values(['sort', 'animal', 'condition'], ascending=True).reset_index(), 'color')
    plt.savefig('conditional_probabilities_color.pdf')
