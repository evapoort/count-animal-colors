# Blind acquisition of animal colors, a corpus study
To replicate the full analysis in the commentary, run the steps in this manual sequentially. Please note that some of the steps are prohibitively memory- or compute-intensive if you execute them on a the average desktop computer. If you just want to play around with the phrase counts and conditional probabilities, start with _Tallying color/animal phrases_ and the files produced in that section.

## Downloading the OpenSubtitles corpus
Run `python download.py en sub` to download the OpenSubtitles corpus in English from OPUS, the Open Parallel Corpus.
Use other two letter ISO language codes to get other languages (e.g., `de` for German, `fr` for French). Use `wiki` instead of `sub` to download Wikipedia corpora. (Caution: the OpenSubtitles corpus is approximately 50GB.)

## Cleaning and deduplicating the OpenSubtitles corpus
Run `python clean_subs.py en --stripxml --join` to clean xml tags out of the corpus and join the individual subtitle files into one large txt file. This is a compute-heavy operation, it could take a long time to run.
Run `python deduplicate.py corpora/sub.en.txt` to deduplicate the corpus. This is a memory intensive operation, run the script with a `--bins=10` flag if you run out of memory (increase number of bins as necessary). Deduplicating is necessary to control for overabundance of subtitle files for very popular movies.

## Tallying color/animal phrases
Run `python count_combos.py corpora/dedup.sub.en.txt` to count color/animal phrases in the OpenSubtitles corpus. This script takes the list of colors and animals it searches for from `animals_colors.tsv`. While the script is searching the corpus, it will print any lines with phrases of interest to your command line.
Run `python analyze_combos.py dedup.sub.en.counts.tsv` to analyze the counts and compute conditional probabilities. This script takes canonical colors from `canonical_colors.tsv`

## Plotting
Run `python plot_probabilities.py dedup.sub.en.results.tsv` to create a plot of the conditional probabilities. The plot will be named `conditional_probabilities_color.pdf` by default.
