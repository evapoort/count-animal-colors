## Sighted people’s language is not helpful for blind individuals’ acquisition of typical animal colors
### Code and corpus repository
The analysis in the letter to the editor is based on the OpenSubtitles corpus, a crowdsourced database of film and television subtitles that represents the --to our knowledge-- largest publically available corpus of transcriptions of pseudoconversational speech. To compute conditional probabilities (i.e., the chance that a given animal will be described as having a particular color), we first count the relevant colors, animals, and animal/color phrases in the corpus. Then, for each animal and color, we divide the number of animal/color occurrences by the number of animal occurrences. The conditional probabilities for the typical color of each animal, and the most common (other) color for each animal is then plotted (you can find the plot in `conditional_probabilities_color.pdf`).  
To replicate the full analysis in the commentary, run the steps in this manual sequentially. Please note that some of the steps are prohibitively memory- or compute-intensive if you execute them on a the average desktop computer.  

**If you just want to play around with the phrase counts and conditional probabilities from the English-language corpus**: Skip points 1, 2, and 3, and start with 4 (_Tallying color/animal phrases_); the count files you need are already included in the repository.

### Downloading the OpenSubtitles corpus
1. `python download.py en sub` to download the OpenSubtitles corpus in English from OPUS, the Open Parallel Corpus. Use other two letter ISO language codes to get other languages (e.g., `de` for German, `fr` for French). Use `wiki` instead of `sub` to download Wikipedia corpora. (Caution: the OpenSubtitles corpus is approximately 50GB.)  
This tool relies on curl, a linux/OSX utility that may not be installed on Windows systems. If you need to download the corpora manually, you can access them through http://opus.nlpl.eu/OpenSubtitles-v2018.php

### Cleaning and deduplicating the OpenSubtitles corpus
2. `python clean_subs.py en --stripxml --join` to clean xml tags out of the corpus and join the individual subtitle files into one large txt file. This is a compute-heavy operation, it could take a long time to run.
3. `python deduplicate.py corpora/sub.en.txt` to deduplicate the corpus. This is a memory intensive operation, run the script with a `--bins=10` flag if you run out of memory (increase number of bins as necessary). Deduplicating is necessary to control for overabundance of subtitle files for very popular movies.

### Tallying color/animal phrases
4. `python count_combos.py corpora/dedup.sub.en.txt` to count color/animal phrases in the OpenSubtitles corpus. This script takes the list of colors and animals it searches for from `animals_colors.tsv`. While the script is searching the corpus, it will print any lines with phrases of interest to your command line.
5. `python analyze_combos.py dedup.sub.en.counts.tsv` to analyze the counts and compute conditional probabilities. This script takes canonical colors from `canonical_colors.tsv`

### Plotting
6. `python plot_probabilities.py dedup.sub.en.results.tsv` to create a plot of the conditional probabilities. The plot will be named `conditional_probabilities_color.pdf` by default.

### Dependencies
The scripts included in this repository will only work with Python 3.6 (or newer), and have a number of external dependencies (numpy, pandas, matplotlib, seaborn, lxml). The latest versions of the dependencies are all available for installation through pip.
